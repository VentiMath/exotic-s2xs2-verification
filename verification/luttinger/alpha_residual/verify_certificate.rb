#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby/standard-library replay of the alpha residual proof.

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
    demand(word[position, left.length] == left,
           "rewrite step #{number} does not match")
    word = word[0...position] + rule.fetch("rhs") +
           (word[(position + left.length)..] || [])
  end
  word
end

def verify_records(proof, relators)
  ngens = proof.fetch("ngens")
  nletters = 2 * ngens
  inverses = proof.fetch("inverse_letters")
  expected = (0...ngens).flat_map { |index| [2 * index + 2, 2 * index + 1] }
  demand(inverses == expected, "invalid inverse-letter table")
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
      source_word = (start...finish).map do |position|
        position.between?(0, lhs_a.length - 1) ? lhs_a[position] : lhs_b[position - offset]
      end
      pos_a = -start
      pos_b = offset - start
      branch_a = source_word[0...pos_a] + first.fetch("rhs") +
                 (source_word[(pos_a + lhs_a.length)..] || [])
      branch_b = source_word[0...pos_b] + second.fetch("rhs") +
                 (source_word[(pos_b + lhs_b.length)..] || [])
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
      demand(reduced_left == derivation.fetch("reduced_left"),
             "left tidy reduction mismatch")
      demand(reduced_right == derivation.fetch("reduced_right"),
             "right tidy reduction mismatch")
      demand(relation_key(left, right) == relation_key(reduced_left, reduced_right),
             "tidy change does not preserve the group equation")
    else
      raise VerificationError, "unknown derivation kind #{derivation['kind'].inspect}"
    end
  end
  records
end

here = File.expand_path(__dir__)
options = { source: File.join(here, "source.json"), negative_controls: false }
OptionParser.new do |parser|
  parser.banner = "Usage: ruby verify_certificate.rb [options] CERTIFICATE"
  parser.on("--source FILE") { |value| options[:source] = File.expand_path(value) }
  parser.on("--negative-controls") { options[:negative_controls] = true }
end.parse!

begin
  demand(ARGV.length == 1, "exactly one certificate path is required")
  certificate_path = File.expand_path(ARGV.fetch(0))
  source_bytes = File.binread(options[:source])
  source = JSON.parse(source_bytes)
  demand(source.fetch("format") == "luttinger-alpha-residual-source-v1",
         "unknown source format")
  factors = source.fetch("word_factors")
  expected_target = free_reduce(
    inverse(factors.fetch("lb_a_y1")) + factors.fetch("geom_A") + factors.fetch("geom_x")
  )
  demand(expected_target.length == 72 && source.fetch("target") == expected_target,
         "source does not encode the stated 72-letter residual")
  demand(source.fetch("ngens") == 3 && source.fetch("relators").length == 78,
         "source is not the sealed complement presentation")

  proof = load_json(certificate_path)
  demand(proof.fetch("format") == "luttinger-alpha-residual-proof-v1",
         "unknown certificate format")
  demand(proof.fetch("source_sha256") == Digest::SHA256.hexdigest(source_bytes),
         "certificate/source digest mismatch")
  demand(proof.fetch("ngens") == source.fetch("ngens"), "generator-count mismatch")
  demand(proof.fetch("relators") == source.fetch("relators"),
         "certificate presentation mismatch")
  demand(proof.fetch("target") == source.fetch("target"), "certificate target mismatch")
  records = verify_records(proof, source.fetch("relators"))
  result = apply_trace(monoid(source.fetch("target")), proof.fetch("target_trace"),
                       records, records.length)
  demand(result.empty?, "target trace does not end at the identity")
  puts "#{certificate_path} VERIFIED ALPHA RESIDUAL IDENTITY " \
       "#{records.length} proof records; #{proof.fetch('target_trace').length} target steps"

  if options[:negative_controls]
    corrupt = Marshal.load(Marshal.dump(proof))
    corrupt.fetch("target_trace").pop
    failed = false
    begin
      damaged = apply_trace(monoid(source.fetch("target")),
                            corrupt.fetch("target_trace"), records, records.length)
      demand(damaged.empty?, "truncated target trace does not end at identity")
    rescue VerificationError
      failed = true
      puts "REJECTED TRUNCATED TARGET TRACE"
    end
    demand(failed, "truncated target trace was accepted")
  end
rescue VerificationError, KeyError, JSON::ParserError, Zlib::GzipFile::Error => e
  warn "VERIFICATION FAILED: #{e.message}"
  exit 1
end
