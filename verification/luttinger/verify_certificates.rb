#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent, standard-library verifier for the two large group-theory proof
# artifacts.  This file intentionally shares no code with the Python
# compiler, model, search programs, or primary certificate checkers.

require "digest"
require "json"
require "optparse"
require "tmpdir"
require "zlib"

class VerificationError < StandardError; end

def demand(condition, message)
  raise VerificationError, message unless condition
end

def read_json(path)
  text = if path.end_with?(".gz")
           Zlib::GzipReader.open(path, &:read)
         else
           File.binread(path)
         end
  JSON.parse(text)
rescue JSON::ParserError, Zlib::GzipFile::Error => e
  raise VerificationError, "cannot decode #{path}: #{e.message}"
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

  variants = [reduced, inverse(reduced)]
  candidates = variants.flat_map do |variant|
    doubled = variant + variant
    (0...variant.length).map { |start| doubled[start, variant.length] }
  end
  candidates.min { |left, right| left <=> right }
end

def check_word(word, nletters, label)
  demand(word.is_a?(Array), "#{label} is not an array")
  demand(word.all? { |letter| letter.is_a?(Integer) && letter.between?(1, nletters) },
         "#{label} contains an invalid monoid letter")
end

def relation_key(left, right)
  signed = lambda do |word|
    word.map do |letter|
      generator = (letter + 1) / 2
      letter.odd? ? generator : -generator
    end
  end
  cyclic_key(signed.call(left) + inverse(signed.call(right)))
end

def apply_trace(original, trace, records, before)
  word = original.dup
  demand(trace.is_a?(Array), "rewrite trace is not an array")
  trace.each_with_index do |step, number|
    demand(step.is_a?(Array) && step.length == 2, "bad rewrite step #{number}")
    rule_id, position = step
    demand(rule_id.is_a?(Integer) && rule_id.between?(0, before - 1),
           "rewrite step #{number} uses an unproved rule")
    demand(position.is_a?(Integer) && position >= 0,
           "rewrite step #{number} has a bad position")
    rule = records[rule_id]
    left = rule.fetch("lhs")
    demand(word[position, left.length] == left,
           "rewrite step #{number} does not match")
    word = word[0...position] + rule.fetch("rhs") +
           (word[(position + left.length)..] || [])
  end
  word
end

def case_slug(filling)
  a = filling.fetch("sign_a").positive? ? "p" : "m"
  b = filling.fetch("sign_b").positive? ? "p" : "m"
  "#{filling.fetch('half_drift')}_#{a}1_#{b}1"
end

def verify_filled_certificate(path, source, source_digest)
  proof = read_json(path)
  demand(proof["format"] == "luttinger-kbmag-proof-v1", "unknown filled-proof format")
  demand(proof["input_sha256"] == source_digest, "filled-proof input digest mismatch")

  index = proof.fetch("case").fetch("index")
  demand(index.is_a?(Integer) && index.between?(0, source.fetch("paper_fillings").length - 1),
         "invalid filling index")
  filling = source.fetch("paper_fillings")[index]
  demand(proof.fetch("case").fetch("slug") == case_slug(filling), "case label mismatch")
  relators = source.fetch("relators") + filling.fetch("relators")
  demand(proof["relators"] == relators, "presentation relators mismatch")
  demand(proof["ngens"] == source["ngens"], "presentation generator count mismatch")

  ngens = proof.fetch("ngens")
  nletters = 2 * ngens
  expected_inverse_letters = (0...ngens).flat_map { |i| [2 * i + 2, 2 * i + 1] }
  inverse_letters = proof.fetch("inverse_letters")
  demand(inverse_letters == expected_inverse_letters, "invalid inverse-letter table")
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
      demand(inverse_letters[left[0] - 1] == left[1], "false inverse axiom")
    when "input_relator"
      relator_index = derivation.fetch("relator")
      demand(relator_index.is_a?(Integer) && relator_index.between?(0, relators.length - 1),
             "invalid input-relator index")
      demand(relation_key(left, right) == input_keys[relator_index],
             "equation does not match claimed input relator")
    when "overlap"
      parent_a = derivation.fetch("parent_a")
      parent_b = derivation.fetch("parent_b")
      demand(parent_a.is_a?(Integer) && parent_a.between?(0, record_id - 1) &&
             parent_b.is_a?(Integer) && parent_b.between?(0, record_id - 1),
             "overlap has an unproved parent")
      first = records[parent_a]
      second = records[parent_b]
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
      position_a = -start
      position_b = offset - start
      branch_a = source_word[0...position_a] + first.fetch("rhs") +
                 (source_word[(position_a + lhs_a.length)..] || [])
      branch_b = source_word[0...position_b] + second.fetch("rhs") +
                 (source_word[(position_b + lhs_b.length)..] || [])
      reduced_a = apply_trace(branch_a, derivation.fetch("trace_a"), records, record_id)
      reduced_b = apply_trace(branch_b, derivation.fetch("trace_b"), records, record_id)
      demand(relation_key(left, right) == relation_key(reduced_a, reduced_b),
             "overlap does not prove recorded equation")
    when "change"
      old_id = derivation.fetch("old")
      demand(old_id.is_a?(Integer) && old_id.between?(0, record_id - 1),
             "changed equation is not previously proved")
      old = records[old_id]
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

  roots = proof.fetch("roots")
  demand(roots.length == nletters, "wrong number of identity roots")
  roots.each_with_index do |record_id, offset|
    demand(record_id.is_a?(Integer) && record_id.between?(0, records.length - 1),
           "invalid identity root")
    demand(records[record_id]["lhs"] == [offset + 1], "identity root has wrong generator")
    demand(records[record_id]["rhs"] == [], "identity root does not end at identity")
  end
  records.length
rescue KeyError => e
  raise VerificationError, "missing filled-proof field: #{e.message}"
end

options = {
  root: File.expand_path(__dir__),
  input: nil,
  expected_count: 8,
  negative_controls: false
}
OptionParser.new do |parser|
  parser.banner = "Usage: ruby verify_certificates.rb [options] [filled-proof.json.gz ...]"
  parser.on("--root DIR", "directory containing r_presentations.json and proof artifacts") do |value|
    options[:root] = File.expand_path(value)
  end
  parser.on("--input FILE", "presentation source JSON (defaults to ROOT/r_presentations.json)") do |value|
    options[:input] = File.expand_path(value)
  end
  parser.on("--expected-count N", Integer,
            "required certificate count (defaults to 8)") do |value|
    options[:expected_count] = value
  end
  parser.on("--negative-controls", "also prove that two deliberate corruptions are rejected") do
    options[:negative_controls] = true
  end
end.parse!

begin
  root = options[:root]
  presentation_path = options[:input] || File.join(root, "r_presentations.json")
  source_bytes = File.binread(presentation_path)
  source = JSON.parse(source_bytes)
  source_digest = Digest::SHA256.hexdigest(source_bytes)
  proof_paths = if ARGV.empty?
                  Dir[File.join(root, "proof_certificates", "*.json.gz")].sort
                else
                  ARGV.map { |path| File.expand_path(path) }
                end
  demand(options[:expected_count].positive?, "expected count must be positive")
  demand(proof_paths.length == options[:expected_count],
         "expected exactly #{options[:expected_count]} filled-group certificates")
  total_records = 0
  proof_paths.each do |path|
    count = verify_filled_certificate(path, source, source_digest)
    total_records += count
    puts "VERIFIED FILLED GROUP #{File.basename(path)} (#{count} records)"
  end

  if options[:negative_controls]
    first_proof = read_json(proof_paths.first)
    reject_mutation = lambda do |label, mutated|
      temporary = File.join(Dir.tmpdir,
                            "luttinger-corrupt-filled-#{Process.pid}.json.gz")
      begin
        Zlib::GzipWriter.open(temporary) { |stream| stream.write(JSON.generate(mutated)) }
        verify_filled_certificate(temporary, source, source_digest)
        raise VerificationError, "corrupted #{label} was accepted"
      rescue VerificationError => error
        demand(error.message != "corrupted #{label} was accepted",
               "corrupted #{label} was accepted")
        puts "REJECTED DELIBERATELY CORRUPTED #{label.upcase}"
      ensure
        File.delete(temporary) if File.exist?(temporary)
      end
    end

    bad_root = Marshal.load(Marshal.dump(first_proof))
    root_id = bad_root.fetch("roots").first
    bad_root.fetch("records")[root_id]["rhs"] = [1]
    reject_mutation.call("identity root", bad_root)

    bad_input = Marshal.load(Marshal.dump(first_proof))
    input_record = bad_input.fetch("records").find do |record|
      record.fetch("proof").fetch("kind") == "input_relator"
    end
    input_record.fetch("lhs") << input_record.fetch("lhs").first
    reject_mutation.call("input-relator equation", bad_input)

    bad_trace = Marshal.load(Marshal.dump(first_proof))
    trace = nil
    bad_trace.fetch("records").each do |record|
      derivation = record.fetch("proof")
      next unless derivation.fetch("kind") == "overlap"
      trace = derivation.fetch("trace_a") unless derivation.fetch("trace_a").empty?
      trace ||= derivation.fetch("trace_b") unless derivation.fetch("trace_b").empty?
      break if trace
    end
    demand(trace, "negative control could not find a nonempty rewrite trace")
    trace.first[1] += 1
    reject_mutation.call("rewrite trace", bad_trace)

    begin
      verify_filled_certificate(proof_paths.first, source, "0" * 64)
      raise VerificationError, "wrong presentation digest was accepted"
    rescue VerificationError => error
      demand(error.message != "wrong presentation digest was accepted",
             "wrong presentation digest was accepted")
      puts "REJECTED WRONG PRESENTATION DIGEST"
    end
  end

  puts "ALL RUBY FILLED-GROUP CHECKS PASSED: #{total_records} DAG records"
rescue VerificationError, KeyError, Errno::ENOENT => e
  warn "VERIFICATION FAILED: #{e.message}"
  exit 1
end
