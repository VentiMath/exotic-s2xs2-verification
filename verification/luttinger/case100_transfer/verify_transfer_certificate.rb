#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby/standard-library replay of the case-100 transfer proof.
# It shares no code with the Python compiler or Python verifier.

require "digest"
require "json"
require "optparse"
require "zlib"

class VerificationError < StandardError; end

def demand(condition, message)
  raise VerificationError, message unless condition
end

def load_json(path)
  text = path.end_with?(".gz") ? Zlib::GzipReader.open(path, &:read) : File.binread(path)
  JSON.parse(text)
end

def inverse(word)
  word.reverse.map { |letter| -letter }
end

def free_reduce(word)
  output = []
  word.each do |letter|
    if !output.empty? && output[-1] == -letter
      output.pop
    else
      output << letter
    end
  end
  output
end

def cyclic_reduce(word)
  output = free_reduce(word)
  output = output[1...-1] while output.length > 1 && output[0] == -output[-1]
  output
end

def cyclic_key(word)
  reduced = cyclic_reduce(word)
  return [] if reduced.empty?

  [reduced, inverse(reduced)].flat_map do |variant|
    doubled = variant + variant
    (0...variant.length).map { |start| doubled[start, variant.length] }
  end.min { |left, right| left <=> right }
end

def monoid(word)
  word.map { |letter| 2 * letter.abs - (letter.positive? ? 1 : 0) }
end

def signed(word)
  word.map do |letter|
    generator = (letter + 1) / 2
    letter.odd? ? generator : -generator
  end
end

def relation_key(left, right)
  cyclic_key(signed(left) + inverse(signed(right)))
end

def check_word(word, nletters, label)
  demand(word.is_a?(Array), "#{label} is not an array")
  demand(word.all? { |letter| letter.is_a?(Integer) && letter.between?(1, nletters) },
         "#{label} contains an invalid monoid letter")
end

def apply_trace(original, trace, records, before)
  word = original.dup
  demand(trace.is_a?(Array), "rewrite trace is not an array")
  trace.each_with_index do |step, number|
    demand(step.is_a?(Array) && step.length == 2, "bad rewrite step #{number}")
    rule_id, position = step
    demand(rule_id.is_a?(Integer) && rule_id >= 0 && rule_id < before,
           "rewrite step #{number} uses an unproved rule")
    demand(position.is_a?(Integer) && position >= 0,
           "rewrite step #{number} has a bad position")
    rule = records.fetch(rule_id)
    left = rule.fetch("lhs")
    demand(word[position, left.length] == left, "rewrite step #{number} does not match")
    word = word[0...position] + rule.fetch("rhs") +
           (word[(position + left.length)..] || [])
  end
  word
end

def verify_records(proof, relators)
  ngens = proof.fetch("ngens")
  nletters = 2 * ngens
  expected_inverses = (0...ngens).flat_map { |i| [2 * i + 2, 2 * i + 1] }
  inverses = proof.fetch("inverse_letters")
  demand(inverses == expected_inverses, "invalid inverse-letter table")
  input_keys = relators.map { |word| cyclic_key(word) }
  records = proof.fetch("records")

  records.each_with_index do |record, record_id|
    left = record.fetch("lhs")
    right = record.fetch("rhs")
    check_word(left, nletters, "record #{record_id} lhs")
    check_word(right, nletters, "record #{record_id} rhs")
    derivation = record.fetch("proof")
    case derivation.fetch("kind")
    when "inverse_axiom"
      demand(right.empty? && left.length == 2, "malformed inverse axiom")
      demand(inverses[left[0] - 1] == left[1], "false inverse axiom")
    when "input_relator"
      index = derivation.fetch("relator")
      demand(index.is_a?(Integer) && index.between?(0, relators.length - 1),
             "invalid input-relator index")
      demand(relation_key(left, right) == input_keys[index],
             "equation does not match claimed input relator")
    when "overlap"
      parent_a = derivation.fetch("parent_a")
      parent_b = derivation.fetch("parent_b")
      demand(parent_a.is_a?(Integer) && parent_a >= 0 && parent_a < record_id &&
             parent_b.is_a?(Integer) && parent_b >= 0 && parent_b < record_id,
             "overlap has an unproved parent")
      first = records.fetch(parent_a)
      second = records.fetch(parent_b)
      lhs_a = first.fetch("lhs")
      lhs_b = second.fetch("lhs")
      offset = derivation.fetch("offset")
      demand(offset.is_a?(Integer) && offset > -lhs_b.length && offset < lhs_a.length,
             "empty or nonintegral overlap")
      low = [0, offset].max
      high = [lhs_a.length, offset + lhs_b.length].min
      demand(lhs_a[low...high] == lhs_b[(low - offset)...(high - offset)],
             "parent left sides do not overlap")
      start = [0, offset].min
      finish = [lhs_a.length, offset + lhs_b.length].max
      source = (start...finish).map do |position|
        position.between?(0, lhs_a.length - 1) ? lhs_a[position] : lhs_b[position - offset]
      end
      pos_a = -start
      pos_b = offset - start
      branch_a = source[0...pos_a] + first.fetch("rhs") +
                 (source[(pos_a + lhs_a.length)..] || [])
      branch_b = source[0...pos_b] + second.fetch("rhs") +
                 (source[(pos_b + lhs_b.length)..] || [])
      reduced_a = apply_trace(branch_a, derivation.fetch("trace_a"), records, record_id)
      reduced_b = apply_trace(branch_b, derivation.fetch("trace_b"), records, record_id)
      demand(relation_key(left, right) == relation_key(reduced_a, reduced_b),
             "overlap does not prove recorded equation")
    when "change"
      old_id = derivation.fetch("old")
      demand(old_id.is_a?(Integer) && old_id >= 0 && old_id < record_id,
             "changed equation is not previously proved")
      old = records.fetch(old_id)
      reduced_left = apply_trace(old.fetch("lhs"), derivation.fetch("left_trace"),
                                 records, record_id)
      reduced_right = apply_trace(old.fetch("rhs"), derivation.fetch("right_trace"),
                                  records, record_id)
      demand(reduced_left == derivation.fetch("reduced_left"), "left tidy reduction mismatch")
      demand(reduced_right == derivation.fetch("reduced_right"), "right tidy reduction mismatch")
      demand(relation_key(left, right) == relation_key(reduced_left, reduced_right),
             "tidy change does not preserve the group equation")
    else
      raise VerificationError, "unknown derivation kind #{derivation['kind'].inspect}"
    end
  end
  records
end

here = File.expand_path(__dir__)
raw = File.expand_path("../raw_j_certificates", here)
options = {
  source: File.join(here, "common_core_source.json"),
  n0: File.join(raw, "n0_y1_ap1_bp1_jap1_jbp1_presentation.json"),
  n1: File.join(raw, "n1_y2_ap1_bp1_jap1_jbp1_presentation.json")
}
OptionParser.new do |parser|
  parser.banner = "Usage: ruby verify_transfer_certificate.rb [options] CERTIFICATE"
  parser.on("--source FILE") { |value| options[:source] = File.expand_path(value) }
  parser.on("--n0 FILE") { |value| options[:n0] = File.expand_path(value) }
  parser.on("--n1 FILE") { |value| options[:n1] = File.expand_path(value) }
end.parse!

begin
  demand(ARGV.length == 1, "exactly one certificate path is required")
  certificate_path = File.expand_path(ARGV.fetch(0))
  source_bytes = File.binread(options[:source])
  source = JSON.parse(source_bytes)
  demand(source.fetch("format") == "luttinger-case100-common-core-v1",
         "unknown source format")
  n0_bytes = File.binread(options[:n0])
  n1_bytes = File.binread(options[:n1])
  demand(Digest::SHA256.hexdigest(n0_bytes) == source.fetch("n0_source_sha256"),
         "n0 source digest mismatch")
  demand(Digest::SHA256.hexdigest(n1_bytes) == source.fetch("n1_source_sha256"),
         "n1 source digest mismatch")
  n0 = JSON.parse(n0_bytes)
  n1 = JSON.parse(n1_bytes)
  core = source.fetch("common_relators")
  demand(n0.fetch("ngens") == 4 && n1.fetch("ngens") == 4 && source.fetch("ngens") == 4,
         "generator-count mismatch")
  demand(core.length == 96, "common core does not contain 96 relators")
  demand(n0.fetch("relators")[1..] == core && n1.fetch("relators")[1..] == core,
         "the frozen presentations do not have the claimed common core")
  demand(n0.fetch("relators")[0] == source.fetch("n0_extra_relator"),
         "n0 extra relator mismatch")
  demand(n1.fetch("relators")[0] == source.fetch("n1_extra_relator"),
         "n1 extra relator mismatch")

  proof = load_json(certificate_path)
  demand(proof.fetch("format") == "luttinger-case100-transfer-proof-v1",
         "unknown certificate format")
  demand(proof.fetch("source_sha256") == Digest::SHA256.hexdigest(source_bytes),
         "certificate/source digest mismatch")
  demand(proof.fetch("ngens") == 4 && proof.fetch("common_relators") == core,
         "certificate presentation mismatch")
  records = verify_records(proof, core)

  expected = {
    "g1" => [[1], []], "g1_inverse" => [[-1], []],
    "g3" => [[3], []], "g3_inverse" => [[-3], []],
    "g4" => [[4], []], "g4_inverse" => [[-4], []],
    "n0_extra" => [source.fetch("n0_extra_relator"), [-2]],
    "n1_extra" => [source.fetch("n1_extra_relator"), [-2]]
  }
  targets = proof.fetch("targets")
  demand(targets.length == expected.length, "wrong number of target equalities")
  seen = {}
  targets.each do |target|
    name = target.fetch("name")
    demand(expected.key?(name) && !seen.key?(name), "unknown or duplicate target equality")
    seen[name] = true
    lhs, rhs = expected.fetch(name)
    demand(target.fetch("lhs") == lhs && target.fetch("rhs") == rhs,
           "false target statement for #{name}")
    result = apply_trace(monoid(lhs), target.fetch("trace"), records, records.length)
    demand(result == monoid(rhs), "target trace failed for #{name}")
  end
  demand(seen.keys.sort == expected.keys.sort, "missing target equality")

  puts "#{certificate_path} VERIFIED CASE 100 TRIVIAL #{records.length} proof records; " \
       "common core 96/97"
rescue VerificationError, KeyError, JSON::ParserError, Zlib::GzipFile::Error => e
  warn "VERIFICATION FAILED: #{e.message}"
  exit 1
end
