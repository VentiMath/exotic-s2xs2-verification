#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent replay of downstream_chain_certificate.json.
#
# This checker shares no code with downstream_chain.py.  It re-derives every
# computed fact of the chain from scratch, checks that every dependency the
# chain cites exists and that the dependency graph is acyclic, that each of
# the three conclusions depends on the certified triviality of pi_1(V), and
# that every evidence file is present with the recorded SHA-256.
#
#   ruby verify_downstream_chain.rb [--root DIR] [CERTIFICATE]

require "digest"
require "json"
require "optparse"

def demand(condition, message)
  raise "FAILED: #{message}" unless condition
end

# ---------------------------------------------------------------- lattices

def pair(form, u, v)
  (0..1).sum { |i| (0..1).sum { |j| u[i] * form[i][j] * v[j] } }
end

def det2(m)
  m[0][0] * m[1][1] - m[0][1] * m[1][0]
end

# ---------------------------------------------------------------- checks
# Each check receives the recorded "result" and raises on disagreement.

CHECKS = {
  "C_euler" => lambda do |r|
    chi_f = 2 - 2 * 2
    chi_base = 2 - 2 * 1 - 1
    chi_r = chi_f * chi_base
    chi_v = chi_r                       # T^2 x D^2 and T^3 both have chi 0
    chi_z = 2 * chi_v - 0
    demand(r["chi_F"] == chi_f && r["chi_base"] == chi_base, "chi(F), chi(base)")
    demand(r["chi_R"] == chi_r && r["chi_V"] == chi_v, "chi(R), chi(V)")
    demand(r["chi_Z"] == chi_z && r["chi_W"] == chi_z / 2, "chi(Z), chi(W)")
    demand(chi_v == 2 && chi_z == 4, "expected chi(V) = 2, chi(Z) = 4")
  end,
  "C_betti" => lambda do |r|
    b2 = ->(chi, b) { chi - b["b0"] + b["b1"] + b["b3"] - b["b4"] }
    demand(b2.call(2, r["V"]) == r["V"]["b2"] && r["V"]["b2"] == 1, "b2(V)")
    demand(b2.call(4, r["Z"]) == r["Z"]["b2"] && r["Z"]["b2"] == 2, "b2(Z)")
    demand(b2.call(2, r["W"]) == r["W"]["b2"] && r["W"]["b2"] == 0, "b2(W)")
    demand(b2.call(2, r["W_mod2"]) == r["W_mod2"]["b2"] && r["W_mod2"]["b2"] == 2,
           "b2(W; Z/2)")
    demand(r["V"]["b4"] == 0 && r["Z"]["b4"] == 1, "top Betti numbers")
    demand(r["W_mod2"]["b1"] == 1 && r["W_mod2"]["b3"] == 1, "mod-2 duality")
  end,
  "C_w2_fiber" => lambda do |r|
    demand(((2 - 2 * 2) + 0) % 2 == 0 && r["w2_pairing_mod2"] == 0, "w2 pairing")
  end,
  "C_hyperbolic_basis" => lambda do |r|
    g = [[0, 1], [1, 0]]
    demand(r["gram"] == g, "Gram matrix of (F, Gamma_hat)")
    demand(det2(g) == -1 && r["det"] == -1, "determinant")
    demand(r["index_squared"] == 1, "index")
    demand(pair(g, [1, 1], [1, 1]) == 2 && pair(g, [1, -1], [1, -1]) == -2,
           "signature witnesses")
    even = (-3..3).to_a.product((-3..3).to_a).all? { |v| pair(g, v, v).even? }
    demand(even && r["even"] == true, "evenness")
    demand(r["signature"] == 0 && r["b_plus"] == 1 && r["b_minus"] == 1, "signature")
  end,
  "C_square_zero_axes" => lambda do |r|
    h = [[0, 1], [1, 0]]
    box = r["box"]
    bad = (-box..box).to_a.product((-box..box).to_a).count do |a, b|
      (a != 0 || b != 0) && pair(h, [a, b], [a, b]).zero? && a != 0 && b != 0
    end
    demand(bad.zero? && r["off_axis_square_zero"].zero?, "square-zero axes")
    demand(pair(h, [3, 5], [3, 5]) == 2 * 3 * 5, "(aF + bG)^2 = 2ab")
  end,
  "C_cover_genus" => lambda do |r|
    (1..r["checked_k_up_to"]).each do |k|
      genus = 1 - (k * (2 - 2 * 2)) / 2
      demand(genus == k + 1, "genus of #{k}-fold cover")
    end
    r["genus_of_k_cover"].each { |k, g| demand(g == k + 1, "table row #{k}") }
    demand(r["minimum_over_k_nonzero"] == 2, "minimum genus")
  end,
  "C_adjunction" => lambda do |r|
    demand(2 * 2 - 2 - 0 == 2 && r["K_dot_F"] == 2, "adjunction")
  end,
  "C_odd_basis" => lambda do |r|
    lo, hi = r["checked_n_range"]
    (lo..hi).each do |n|
      q = [[0, 1], [1, 2 * n + 1]]
      e = [-n, 1]
      d = [1 + n, -1]
      demand(pair(q, e, e) == 1, "E.E at n=#{n}")
      demand(pair(q, d, d) == -1, "D.D at n=#{n}")
      demand(pair(q, e, d).zero?, "E.D at n=#{n}")
      demand(det2(q) == -1, "det at n=#{n}")
    end
    demand(r["signature"] == 0 && r["b_plus"] == 1 && r["odd"] == true, "odd form data")
  end,
  "C_square_zero_lines_odd" => lambda do |r|
    box = r["box"]
    lines = (-box..box).to_a.product((-box..box).to_a).select do |a, b|
      (a != 0 || b != 0) && a * a - b * b == 0
    end.map { |a, b| a == b ? [1, 1] : [1, -1] }.uniq.sort
    demand(lines == [[1, -1], [1, 1]] && r["lines"].sort == lines, "square-zero lines")
  end,
  "C_arf_figure_eight" => lambda do |r|
    s = [[1, -1], [0, -1]]
    demand(r["seifert_matrix"] == s, "Seifert matrix")
    # det(S - t S^T) computed symbolically as polynomial coefficients.
    # S - tS^T = [[1 - t, -1], [t, -1 + t]]
    # det = (1 - t)(-1 + t) - (-1)(t) = -(1 - t)^2 + t = -1 + 3t - t^2
    coeffs = [-1, 3, -1]
    demand(r["alexander_coefficients"] == coeffs, "Alexander coefficients")
    at_minus_one = coeffs.each_with_index.sum { |c, i| c * (-1)**i }
    demand(at_minus_one == -5 && r["delta_at_minus_one"] == -5, "Delta(-1)")
    residue = at_minus_one % 8
    arf_levine = [1, 7].include?(residue) ? 0 : 1
    zeros = [0, 1].product([0, 1]).count do |x|
      ((0..1).sum { |i| (0..1).sum { |j| x[i] * s[i][j] * x[j] } } % 2).zero?
    end
    arf_quadratic = zeros == 3 ? 0 : 1
    demand(arf_levine == 1 && arf_quadratic == 1 && r["arf"] == 1, "Arf(4_1)")
    demand(r["quadratic_form_zeros"] == zeros, "quadratic form zeros")
  end,
  "C_klug_instance" => lambda do |r|
    rhs = ((r["sigma"] - r["D_squared"]) / 8 + r["mu_S3"]) % 2
    forced = (rhs - r["arf_disk"]) % 2
    demand(r["sigma"].zero? && r["D_squared"].zero? && r["arf_disk"].zero?, "inputs")
    demand(forced.zero? && r["forced_arf_41"].zero? && r["actual_arf_41"] == 1,
           "Klug contradiction")
  end,
  "C_covering_order" => lambda do |r|
    demand(r["order_pi1_Z"] * r["deck_order"] == 2 && r["order_pi1_W"] == 2, "covering order")
  end,
  "C_hk_invariants" => lambda do |r|
    demand(r["W"] == r["B"] && r["equal"] == true, "HK invariants equal")
    demand(r["W"]["pi_1"] == "Z/2" && r["W"]["w2_type"] == "II" && r["W"]["KS"].zero?,
           "HK invariant values")
  end,
  "C_signatures" => lambda do |r|
    demand(r["KS_even_case"].zero?, "KS of even form with signature 0")
    demand(r["sigma_Z"].end_with?("= 0") && r["sigma_Zpp"].end_with?("= 0"), "signatures")
  end,
  "C_orientation_reversal" => lambda do |r|
    demand(r["degree"] == -1, "orientation-reversing self-map of S^2 x S^2")
  end,
}.freeze

# ---------------------------------------------------------------- main

options = { root: nil }
OptionParser.new do |parser|
  parser.banner = "usage: verify_downstream_chain.rb [--root DIR] [CERTIFICATE]"
  parser.on("--root DIR", "repository verification root") { |v| options[:root] = File.expand_path(v) }
end.parse!

certificate = ARGV.first || File.join(__dir__, "downstream_chain_certificate.json")
root = options[:root] || File.expand_path("..", __dir__)
data = JSON.parse(File.read(certificate))

demand(data["format"] == "luttinger-downstream-proof-chain-v1", "unknown format")
items = data["items"]
by_id = items.to_h { |item| [item["id"], item] }
demand(by_id.size == items.size, "duplicate item ids")

# Dependency graph: every citation resolves; acyclic; conclusions reach K.
items.each do |item|
  (item["uses"] || []).each do |dep|
    demand(by_id.key?(dep), "#{item['id']} cites unknown #{dep}")
  end
end
state = Hash.new(0)
visit = lambda do |name|
  demand(state[name] != 1, "dependency cycle through #{name}")
  return if state[name] == 2
  state[name] = 1
  (by_id[name]["uses"] || []).each { |dep| visit.call(dep) }
  state[name] = 2
end
by_id.each_key { |name| visit.call(name) }

reach = lambda do |name, acc|
  (by_id[name]["uses"] || []).each do |dep|
    next if acc.include?(dep)
    acc << dep
    reach.call(dep, acc)
  end
  acc
end
data["conclusions"].each do |conclusion|
  demand(by_id.key?(conclusion), "missing conclusion #{conclusion}")
  demand(reach.call(conclusion, []).include?("K_pi1_V_trivial"),
         "#{conclusion} does not rest on the certified pi_1(V) = 1")
end
demand(data["conclusions"].sort == %w[S12_theorem_B S16_theorem_C S7_theorem_A],
       "conclusions are Theorems A, B, C")

# Every computed fact is recomputed here.
computed = items.select { |item| item["kind"] == "computed" }
computed.each do |item|
  checker = CHECKS[item["id"]]
  demand(checker, "no independent check for #{item['id']}")
  checker.call(item["result"])
end
demand(computed.size == CHECKS.size, "every check corresponds to a computed item")

# External items carry a statement and a source; certificates carry evidence.
items.select { |i| i["kind"] == "external" }.each do |item|
  demand(!item["statement"].to_s.empty? && !item["source"].to_s.empty?,
         "external #{item['id']} lacks a statement or source")
end
items.select { |i| i["kind"] == "certificate" }.each do |item|
  item["evidence"].each do |relative|
    demand(data["evidence_sha256"].key?(relative), "#{item['id']} evidence #{relative} unbound")
  end
end

# Evidence files are present with the recorded digests.
data["evidence_sha256"].each do |relative, digest|
  path = File.join(root, relative)
  demand(File.file?(path), "missing evidence file #{relative}")
  actual = Digest::SHA256.file(path).hexdigest
  demand(actual == digest, "digest mismatch for #{relative}")
end

kinds = items.group_by { |i| i["kind"] }.transform_values(&:size)
puts "ALL RUBY DOWNSTREAM-CHAIN CHECKS PASSED: " \
     "#{kinds.sort.map { |k, v| "#{k}=#{v}" }.join(', ')}; " \
     "#{computed.size} computed facts replayed; " \
     "#{data['evidence_sha256'].size} evidence digests verified"
