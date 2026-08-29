#!/usr/bin/env ruby
# frozen_string_literal: true

# Second-language verifier for the raw-complex-to-four-generator transport.
# Shares no code with verify_tietze_transport.py, fast_tietze.py, or any
# project module.  Checks r_tietze_input.json.gz against
# r_tietze_certificate.json.gz and r_presentations.json exactly as the Python
# verifier does: input digest, every elementary elimination, output digest,
# and equality with the committed renumbered presentation.
#
#   ruby verify_tietze_transport.rb [--root DIR] [--negative-controls]

require "digest"
require "json"
require "optparse"
require "zlib"

class VerificationError < StandardError; end

def demand(condition, message)
  raise VerificationError, message unless condition
end

def digest(payload)
  Digest::SHA256.hexdigest(JSON.generate(payload))
end

def load_json(path)
  text = path.end_with?(".gz") ? Zlib::GzipReader.open(path, &:read) : File.read(path)
  JSON.parse(text)
end

def inverse(word)
  word.reverse.map { |x| -x }
end

def free_reduce(word)
  out = []
  word.each do |x|
    if !out.empty? && out.last == -x
      out.pop
    else
      out << x
    end
  end
  out
end

def cyclic_reduce(word)
  word = free_reduce(word)
  word = word[1...-1] while word.length >= 2 && word.first == -word.last
  word
end

def replay(source, certificate)
  ngens = source.fetch("ngens")
  relators = source.fetch("relators")
  words = source.fetch("words")
  demand(certificate["format"] == "luttinger-fast-tietze-v1", "unknown certificate format")
  demand(certificate["ngens"] == ngens, "generator count mismatch")
  demand(certificate["input_sha256"] == digest([ngens, relators, words]),
         "certificate does not belong to this input")
  steps = certificate.fetch("steps")
  demand(certificate["steps_count"] == steps.length, "step count mismatch")
  relators.each_with_index do |relator, index|
    relator.each do |letter|
      demand(letter.is_a?(Integer) && letter.abs.between?(1, ngens),
             "relator #{index} uses an invalid letter")
    end
  end

  rels = {}
  relators.each_with_index do |relator, index|
    reduced = cyclic_reduce(relator)
    rels[index] = reduced unless reduced.empty?
  end
  tracked = words.map { |w| free_reduce(w) }
  occ = Hash.new { |h, k| h[k] = {} }
  rels.each { |i, r| r.map(&:abs).uniq.each { |g| occ[g][i] = true } }

  steps.each_with_index do |step, k|
    number = k + 1
    demand(step.is_a?(Array) && step.length == 3, "step #{number}: malformed")
    i, g, recorded = step
    demand(rels.key?(i), "step #{number}: source relator #{i} is absent")
    relator = rels[i]
    positions = relator.each_index.select { |p| relator[p].abs == g }
    demand(positions.length == 1, "step #{number}: generator #{g} does not occur exactly once")
    pos = positions.first
    expected = inverse(relator[0...pos]) + inverse(relator[(pos + 1)..])
    expected = inverse(expected) if relator[pos].negative?
    demand(recorded == expected, "step #{number}: replacement is not implied by the relator")

    substitute = lambda do |word|
      out = []
      word.each do |h|
        if h == g then out.concat(recorded)
        elsif h == -g then out.concat(inverse(recorded))
        else out << h
        end
      end
      free_reduce(out)
    end

    targets = occ.key?(g) ? occ[g].keys : []
    rels[i].map(&:abs).uniq.each { |h| occ[h].delete(i) if occ.key?(h) }
    rels.delete(i)
    targets.each do |j|
      next if j == i || !rels.key?(j)
      rels[j].map(&:abs).uniq.each { |h| occ[h].delete(j) if occ.key?(h) }
      replaced = cyclic_reduce(substitute.call(rels[j]))
      if replaced.empty?
        rels.delete(j)
      else
        rels[j] = replaced
        replaced.map(&:abs).uniq.each { |h| occ[h][j] = true }
      end
    end
    tracked = tracked.map { |w| substitute.call(w) }
    occ.delete(g)
  end

  seen = {}
  out = []
  rels.each_value do |relator|
    next if seen.key?(relator) || seen.key?(inverse(relator))
    seen[relator] = true
    out << relator
  end
  live = (out.flatten.map(&:abs) + tracked.flatten.map(&:abs)).uniq.sort
  demand(certificate["output_sha256"] == digest([live, out, tracked]),
         "replayed output does not match the certificate's output digest")
  [live, out, tracked]
end

def check_against_committed(live, out, tracked, names, presentation)
  renumbering = live.sort.each_with_index.to_h { |g, k| [g, k + 1] }
  demand(renumbering.transform_keys(&:to_s) == presentation.fetch("renumbering"), "renumbering mismatch")
  renumber = ->(word) { word.map { |g| renumbering.fetch(g.abs) * (g.positive? ? 1 : -1) } }
  demand(presentation.fetch("ngens") == live.length, "committed generator count mismatch")
  demand(out.map(&renumber) == presentation.fetch("relators"),
         "committed complement relators differ from the replayed output")
  committed_words = presentation.fetch("tracked_words")
  demand(names.length == tracked.length, "tracked word name count mismatch")
  demand(names.uniq.length == names.length, "duplicate tracked word name")
  demand(names.sort == committed_words.keys.sort,
         "committed tracked word names differ from the sealed input")
  names.zip(tracked).each do |name, word|
    demand(renumber.call(word) == committed_words.fetch(name),
           "committed tracked word #{name} differs from the replayed output")
  end
  [out.length, committed_words.length]
end

options = { root: File.join(__dir__, "sealed_transport"), negative_controls: false }
OptionParser.new do |parser|
  parser.on("--root DIR") { |v| options[:root] = File.expand_path(v) }
  parser.on("--negative-controls") { options[:negative_controls] = true }
end.parse!

begin
  root = options[:root]
  source = load_json(File.join(root, "r_tietze_input.json.gz"))
  demand(source["format"] == "luttinger-tietze-input-v1", "unknown input format")
  demand(source["word_names"].is_a?(Array), "sealed input lacks tracked word names")
  certificate = load_json(File.join(root, "r_tietze_certificate.json.gz"))
  presentation = load_json(File.join(root, "r_presentations.json"))
  demand(presentation["tietze_certificate"] == "r_tietze_certificate.json.gz",
         "committed presentation names a different certificate")
  live, out, tracked = replay(source, certificate)
  names = source.fetch("word_names")
  relators, words = check_against_committed(live, out, tracked, names, presentation)
  puts "RUBY TIETZE TRANSPORT VERIFIED: #{source['ngens']} generators, " \
       "#{source['relators'].length} relators -> #{live.length} generators, " \
       "#{relators} relators, #{words} tracked words after " \
       "#{certificate['steps_count']} certified eliminations; committed r_presentations.json matches"

  if options[:negative_controls]
    expect_rejection = lambda do |label, fn|
      begin
        fn.call
      rescue VerificationError => e
        puts "REJECTED #{label.upcase}: #{e.message}"
      else
        raise VerificationError, "#{label} was accepted"
      end
    end
    bad_input = JSON.parse(JSON.generate(source))
    bad_input["relators"][0][0] = -bad_input["relators"][0][0]
    expect_rejection.call("corrupted input relator", -> { replay(bad_input, certificate) })
    omitted = JSON.parse(JSON.generate(certificate))
    omitted["steps"].shift
    omitted["steps_count"] -= 1
    expect_rejection.call("omitted elimination step", -> { replay(source, omitted) })
    altered = JSON.parse(JSON.generate(certificate))
    altered["steps"][0][2] = altered["steps"][0][2] + [source["ngens"]]
    expect_rejection.call("altered substitution", -> { replay(source, altered) })
    bad_output = JSON.parse(JSON.generate(presentation))
    bad_output["relators"][0] = bad_output["relators"][0].reverse
    expect_rejection.call("altered committed output",
                          -> { check_against_committed(live, out, tracked, names, bad_output) })
    bad_word = JSON.parse(JSON.generate(presentation))
    longest = bad_word["tracked_words"].max_by { |_, word| word.length }.first
    bad_word["tracked_words"][longest] = bad_word["tracked_words"][longest].reverse
    expect_rejection.call("altered committed tracked word",
                          -> { check_against_committed(live, out, tracked, names, bad_word) })
  end
rescue VerificationError, KeyError, Errno::ENOENT, Zlib::GzipFile::Error => e
  warn "VERIFICATION FAILED: #{e.message}"
  exit 1
end
