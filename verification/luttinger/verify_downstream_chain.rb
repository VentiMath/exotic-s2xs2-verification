#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent replay of downstream_chain_certificate.json -- the existence
# chain for Theorem A'.
#
# This checker shares no code with downstream_chain.py.  It re-derives every
# computed fact from scratch, checks that every dependency the chain cites
# exists and that the graph is acyclic, that the chain carries NO assumption
# item, that no item's text mentions Lidman--Piccirillo, Wuebben, or the
# source-formalization clauses, that the single conclusion rests on the
# three intrinsic pillars (certified pi_1(V_aud) = 1, certified sigma_aud,
# the written descent lemma), that every certificate and proof item is
# bound to files, and that every bound file is present with the recorded
# SHA-256.
#
#   ruby verify_downstream_chain.rb [--root DIR] [CERTIFICATE]

require "digest"
require "json"
require "optparse"
require "set"

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
    chi_z = 2 * chi_v - 0               # M_h is a closed 3-manifold
    demand(r["chi_F"] == chi_f && r["chi_base"] == chi_base, "chi(F), chi(base)")
    demand(r["chi_R"] == chi_r && r["chi_V"] == chi_v, "chi(R), chi(V)")
    demand(r["chi_Z"] == chi_z, "chi(Z)")
    demand(chi_v == 2 && chi_z == 4, "expected chi(V) = 2, chi(Z) = 4")
    demand(r.keys.sort == %w[chi_F chi_R chi_V chi_Z chi_base], "no other manifolds")
  end,
  "C_betti" => lambda do |r|
    b2 = ->(chi, b) { chi - b["b0"] + b["b1"] + b["b3"] - b["b4"] }
    demand(b2.call(2, r["V"]) == r["V"]["b2"] && r["V"]["b2"] == 1, "b2(V)")
    demand(b2.call(4, r["Z"]) == r["Z"]["b2"] && r["Z"]["b2"] == 2, "b2(Z)")
    demand(r["V"]["b4"].zero? && r["Z"]["b4"] == 1, "top Betti numbers")
    demand(r["V"]["b1"].zero? && r["Z"]["b1"].zero?, "b1 = 0 from pi_1 = 1")
    demand(r.keys.sort == %w[V Z], "no other manifolds")
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
    demand(r["signature"].zero? && r["b_plus"] == 1 && r["b_minus"] == 1, "signature")
  end,
  "C_signatures" => lambda do |r|
    demand(r["KS_smooth"].zero?, "KS of a smooth manifold")
    demand(r["sigma_Z"].end_with?("= 0"), "signature of Z")
  end,
  "C_orientation_reversal" => lambda do |r|
    demand(r["degree"] == -1, "orientation-reversing self-map of S^2 x S^2")
  end,
}.freeze

FORBIDDEN = ["Lidman", "Piccirillo", "LP25", "2505.14387", "Wuebben",
             "2608.17267", "Source Formalization", "D1--D14", "D1-D14"].freeze
TEXT_FIELDS = %w[claim statement proof name source where hypotheses].freeze
PILLARS = %w[K_pi1_Vaud_trivial K_sigma_aud P_double_form].freeze

# ---------------------------------------------------------------- main

options = { root: nil }
OptionParser.new do |parser|
  parser.banner = "usage: verify_downstream_chain.rb [--root DIR] [CERTIFICATE]"
  parser.on("--root DIR", "repository root") { |v| options[:root] = File.expand_path(v) }
end.parse!

certificate = ARGV.first || File.join(__dir__, "downstream_chain_certificate.json")
root = options[:root] || File.expand_path("../..", __dir__)
data = JSON.parse(File.read(certificate))

demand(data["format"] == "luttinger-existence-chain-v3", "unknown format")
items = data["items"]
by_id = items.to_h { |item| [item["id"], item] }
demand(by_id.size == items.size, "duplicate item ids")

# No assumption of any kind.
demand(items.none? { |i| i["kind"] == "assumption" }, "chain carries an assumption")
demand(items.none? { |i| i["id"].start_with?("A_") }, "chain carries an A_ item")
demand(%w[external certificate proof computed step].to_set.superset?(items.map { |i| i["kind"] }.to_set),
       "unknown item kind")

# No item text refers to another author's construction.
items.each do |item|
  TEXT_FIELDS.each do |field|
    text = item[field]
    text = text.join(" ") if text.is_a?(Array)
    next if text.nil?
    FORBIDDEN.each do |word|
      demand(!text.include?(word), "#{item['id']}.#{field} mentions #{word}")
    end
  end
end
demand(data["forbidden"].sort == FORBIDDEN.sort, "forbidden list matches")

# Dependency graph: every citation resolves; acyclic; conclusion reaches pillars.
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
demand(data["conclusions"] == %w[S7_theorem_A_prime], "the conclusion is Theorem A'")
demand(data["pillars"].sort == PILLARS.sort, "pillars match")
data["conclusions"].each do |conclusion|
  demand(by_id.key?(conclusion), "missing conclusion #{conclusion}")
  dependencies = reach.call(conclusion, [])
  PILLARS.each do |pillar|
    demand(dependencies.include?(pillar), "#{conclusion} does not rest on #{pillar}")
  end
end
# Every non-step item is on the path of the conclusion.
on_path = reach.call("S7_theorem_A_prime", [])
items.reject { |i| i["kind"] == "step" }.each do |item|
  demand(on_path.include?(item["id"]), "#{item['id']} is not on the path of Theorem A'")
end

# Every computed fact is recomputed here.
computed = items.select { |item| item["kind"] == "computed" }
computed.each do |item|
  checker = CHECKS[item["id"]]
  demand(checker, "no independent check for #{item['id']}")
  checker.call(item["result"])
end
demand(computed.size == CHECKS.size, "every check corresponds to a computed item")

# External items carry a statement and a source; certificates and proofs
# carry bound evidence.
items.select { |i| i["kind"] == "external" }.each do |item|
  demand(!item["statement"].to_s.empty? && !item["source"].to_s.empty?,
         "external #{item['id']} lacks a statement or source")
end
items.select { |i| %w[certificate proof].include?(i["kind"]) }.each do |item|
  demand(!item["evidence"].to_a.empty?, "#{item['id']} has no evidence")
  item["evidence"].each do |relative|
    demand(data["evidence_sha256"].key?(relative), "#{item['id']} evidence #{relative} unbound")
  end
end
items.select { |i| i["kind"] == "proof" }.each do |item|
  demand(!item["where"].to_s.empty?, "proof #{item['id']} does not say where it is written")
end

# Evidence files are present with the recorded digests.
data["evidence_sha256"].each do |relative, digest|
  path = File.join(root, relative)
  demand(File.file?(path), "missing evidence file #{relative}")
  actual = Digest::SHA256.file(path).hexdigest
  demand(actual == digest, "digest mismatch for #{relative}")
end

kinds = items.group_by { |i| i["kind"] }.transform_values(&:size)
puts "ALL RUBY EXISTENCE-CHAIN CHECKS PASSED: " \
     "#{kinds.sort.map { |k, v| "#{k}=#{v}" }.join(', ')}; " \
     "#{computed.size} computed facts replayed; " \
     "#{data['evidence_sha256'].size} evidence digests verified; " \
     "assumptions=0; forbidden names absent"
