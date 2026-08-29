"""Reproducible attacks on the triangulation-derived filled presentations.

The input is ``r_presentations.json``, written by ``r_run.py``.  This driver
generates a small GAP program for one bounded method and runs it through the
configured ``gap`` executable.  No method is treated as a proof unless it
emits an explicit successful condition (zero generators after a certified
Tietze chain, every generator rewriting to one, or a completed coset table).

Examples:
  python3 group_attack.py summary
  python3 group_attack.py kb --case 0
  python3 group_attack.py ace --case 0 --workspace 25000000
  python3 group_attack.py quotients --case 0
  python3 group_attack.py paper-kb-all
"""
import argparse
import hashlib
import json
import os
import subprocess


def gap_word(word):
    if not word:
        return "One(F)"
    return "*".join(
        f"F.{abs(letter)}" + ("^-1" if letter < 0 else "")
        for letter in word)


def load_presentations(path):
    with open(path, encoding="ascii") as stream:
        data = json.load(stream)
    assert data["format"] == "luttinger-filled-presentations-v1"
    return data


def case_setup(data, case):
    filling = data["fillings"][case]
    relators = data["relators"] + filling["relators"]
    setup = f"F := FreeGroup({data['ngens']});;\n"
    setup += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
    setup += "G := F/rels;;\n"
    setup += (f'Print("case {case}: drift={filling["drift"]} '
              f'signs=({filling["sign_a"]},{filling["sign_b"]})\\n");\n')
    setup += "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
    setup += "fg := FreeGeneratorsOfFpGroup(H);; rl := RelatorsOfFpGroup(H);;\n"
    setup += ('Print("  H1=",AbelianInvariants(H)," simplified=",Length(fg),'
              '" gens/",Length(rl)," rels total_length=",Sum(rl,Length),"\\n");\n')
    return setup


def gap_program(data, method, case, workspace, word_name=None):
    if method == "direct-paper-replay":
        assert "paper_fillings" in data
        body = 'LoadPackage("kbmag");;\nall_ok := true;;\n'
        for filling in data["paper_fillings"]:
            slug = (f'{filling["half_drift"]}_'
                    f'{"p" if filling["sign_a"] > 0 else "m"}1_'
                    f'{"p" if filling["sign_b"] > 0 else "m"}1')
            body += f'rws := ReadRWS("direct_rws/{slug}.rws");;\n'
            body += r'''ResetRWS(rws);;
attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
freegens := GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws));;
reductions := List(freegens,z->ReducedForm(rws,z));;
ok := attempt=[true,true] and IsConfluent(rws) and ForAll(reductions,IsOne);;
'''
            body += (f'Print("replay {slug}: KB=",attempt,'
                     '", confluent=",IsConfluent(rws),'
                     '" generator_normal_forms=",reductions," ok=",ok,"\\n");\n'
                     'if not ok then all_ok := false; fi;\n')
        body += ('if not all_ok then Error("exported rewriting-system replay '
                 'failed"); fi;\n'
                 'Print("ALL EIGHT EXPORTED SYSTEMS REPLAYED\\n");\nQUIT;;\n')
        return body

    if method == "direct-paper-export":
        assert "paper_fillings" in data, \
            "rerun r_run.py to export coherent direct paper fillings"
        body = 'LoadPackage("kbmag");;\nall_ok := true;;\n'
        for filling in data["paper_fillings"]:
            hard = (filling["half_drift"] == "n0_y1" and
                    filling["sign_a"] == 1 and filling["sign_b"] == 1)
            ordering = "base_then_fill" if hard else "fill_then_base"
            if hard:
                relators = data["relators"] + filling["relators"]
            else:
                relators = filling["relators"] + data["relators"]
            slug = (f'{filling["half_drift"]}_'
                    f'{"p" if filling["sign_a"] > 0 else "m"}1_'
                    f'{"p" if filling["sign_b"] > 0 else "m"}1')
            prefix = f"direct_rws/{slug}"
            body += f"F := FreeGroup({data['ngens']});;\n"
            body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
            body += ("G := F/rels;;\n"
                     "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
                     "fg := FreeGeneratorsOfFpGroup(H);; "
                     "rl := RelatorsOfFpGroup(H);;\n")
            body += (f'Print("export {slug} ({ordering}): ",Length(fg),'
                     '" gens/",Length(rl)," rels\\n");\n')
            body += (f'PrintTo("{prefix}.presentation",'
                     f'"case := \\"{slug}\\";;\\n",'
                     f'"ordering := \\"{ordering}\\";;\\n",'
                     '"free_generators := ",fg,";;\\n",'
                     '"relators := ",rl,";;\\n");\n')
            body += f'if Length(fg)=0 then\n  PrintTo("{prefix}.certificate",'
            body += ('"certificate := \\"Tietze_zero_generators\\";;\\n");\n'
                     'else\n'
                     '  rws := KBMAGRewritingSystem(H);;\n'
                     '  attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;\n'
                     '  reductions := List(GeneratorsOfGroup('
                     'FreeStructureOfRewritingSystem(rws)),\n'
                     '                     z -> ReducedForm(rws,z));;\n'
                     '  ok := IsConfluent(rws) and ForAll(reductions,IsOne);;\n')
            body += (f'  PrintTo("{prefix}.certificate",'
                     '"knuth_bendix_return := ",attempt,";;\\n",'
                     '"confluent := ",IsConfluent(rws),";;\\n",'
                     '"generator_normal_forms := ",reductions,";;\\n",'
                     '"certified_trivial := ",ok,";;\\n");\n')
            body += (f'  if ok then WriteRWS(rws,"{prefix}.rws");\n'
                     '  else all_ok := false; fi;\n'
                     'fi;\n')
        body += ('if not all_ok then Error("at least one export case did not '
                 'certify trivial"); fi;\n'
                 'Print("ALL EIGHT EXPORTS CERTIFIED\\n");\nQUIT;;\n')
        return body

    if method == "direct-paper-kb-hard":
        assert "paper_fillings" in data
        filling = next(item for item in data["paper_fillings"]
                       if item["half_drift"] == "n0_y1" and
                       item["sign_a"] == 1 and item["sign_b"] == 1)
        fills, base = filling["relators"], data["relators"]
        variants = [
            ("base_then_fill", base + fills),
            ("reverse_base", list(reversed(base)) + fills),
            ("short_first", sorted(base + fills, key=len)),
            ("long_first", sorted(base + fills, key=len, reverse=True)),
        ]
        body = 'LoadPackage("kbmag");;\ndone := false;;\n'
        for name, relators in variants:
            body += "if not done then\n"
            body += f"F := FreeGroup({data['ngens']});;\n"
            body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
            body += ("G := F/rels;;\n"
                     "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
                     "fg := FreeGeneratorsOfFpGroup(H);; "
                     "rl := RelatorsOfFpGroup(H);;\n")
            body += (f'Print("direct hard {name}: ",Length(fg)," gens/",'
                     'Length(rl)," rels\\n");\n')
            body += r'''
if Length(fg)=0 then
  Print("  CERTIFIED TRIVIAL (Tietze)\n"); done := true;
else
  rws := KBMAGRewritingSystem(H);;
  attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
  reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                     z -> ReducedForm(rws,z));;
  Print("  KB returned=",attempt," confluent=",IsConfluent(rws),
        " generator_normal_forms=",reductions,"\n");
  if ForAll(reductions,IsOne) then
    Print("  CERTIFIED TRIVIAL: every generator rewrites to identity\n");
    done := true;
  else Print("  INCONCLUSIVE\n"); fi;
fi;
fi;
'''
        return body + "QUIT;;\n"

    if method == "direct-paper-kb-all":
        assert "paper_fillings" in data, \
            "rerun r_run.py to export coherent direct paper fillings"
        body = 'LoadPackage("kbmag");;\n'
        for i, filling in enumerate(data["paper_fillings"]):
            # Filling-first ordering is the successful certificate ordering
            # for the one otherwise hard adjacent case.
            relators = filling["relators"] + data["relators"]
            body += f"F := FreeGroup({data['ngens']});;\n"
            body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
            body += ("G := F/rels;;\n"
                     "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
                     "fg := FreeGeneratorsOfFpGroup(H);; "
                     "rl := RelatorsOfFpGroup(H);;\n")
            body += (f'Print("direct paper {filling["half_drift"]} '
                     f'({filling["sign_a"]:+d},{filling["sign_b"]:+d}): ",'
                     'Length(fg)," gens/",Length(rl)," rels\\n");\n')
            body += r'''
if Length(fg)=0 then
  Print("  CERTIFIED TRIVIAL (Tietze)\n");
else
  rws := KBMAGRewritingSystem(H);;
  attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
  reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                     z -> ReducedForm(rws,z));;
  Print("  KB returned=",attempt," confluent=",IsConfluent(rws),
        " generator_normal_forms=",reductions,"\n");
  if ForAll(reductions,IsOne) then
    Print("  CERTIFIED TRIVIAL: every generator rewrites to identity\n");
  else Print("  INCONCLUSIVE\n"); fi;
fi;
'''
        return body + "QUIT;;\n"

    if method == "local-paper-inclusion-all":
        def inv(word):
            return [-letter for letter in reversed(word)]

        def signed(word, sign):
            return word if sign > 0 else inv(word)

        tracked = data["tracked_words"]
        alpha_dirs = {
            "n0_Ax": tracked["geom_A"] + tracked["geom_x"],
            "n1_Arinv": tracked["geom_A"] + inv(tracked["geom_r"]),
        }
        beta_dir = (inv(tracked["geom_r"]) + tracked["geom_M"] +
                    tracked["geom_r"] + tracked["geom_B"])
        paper_cases = []
        for alpha_name, alpha_dir in alpha_dirs.items():
            for sign_a in (1, -1):
                for sign_b in (1, -1):
                    paper_cases.append((
                        f"{alpha_name}({sign_a:+d},{sign_b:+d})",
                        [tracked["geom_M"] + signed(alpha_dir, sign_a),
                         tracked["geom_N"] + signed(beta_dir, sign_b)]))

        body = 'LoadPackage("kbmag");;\n'
        gap_names = ",".join(f'"{name}"' for name, _ in paper_cases)
        gap_pairs = ",".join(
            "[" + ",".join(gap_word(word) for word in pair) + "]"
            for _, pair in paper_cases)
        for i, filling in enumerate(data["fillings"]):
            relators = filling["relators"] + data["relators"]
            body += f"F := FreeGroup({data['ngens']});;\n"
            body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
            body += r'''G := F/rels;;
iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;
hom := GroupHomomorphismByImages(F,G,GeneratorsOfGroup(F),
                                 GeneratorsOfGroup(G));;
rws := KBMAGRewritingSystem(H);;
attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
freegens := GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws));;
tofree := function(w) local letters;
  letters := LetterRepAssocWord(UnderlyingElement(w));
  if Length(letters)=0 then return One(freegens[1]); fi;
  return Product(letters,i->freegens[AbsInt(i)]^SignInt(i));
end;;
'''
            body += f"names := [{gap_names}];;\n"
            body += f"wPairs := [{gap_pairs}];;\n"
            body += r'''wHs := List(wPairs,pair->List(pair,
  w->Image(iso,Image(hom,w))));;
normals := List(wHs,pair->List(pair,w->ReducedForm(rws,tofree(w))));;
'''
            body += (f'Print("local case {i}: drift={filling["drift"]} '
                     f'signs=({filling["sign_a"]:+d},{filling["sign_b"]:+d}) '
                     'KB=",attempt," confluent=",IsConfluent(rws),"\\n");\n')
            body += r'''matched := false;;
for j in [1..Length(names)] do
  if ForAll(normals[j],IsOne) then
    Print("  PAPER RELATOR PAIR INCLUDED: ",names[j],
          "  CERTIFIED LOCAL TRIVIAL\n");
    matched := true;
  fi;
od;
if not matched then Print("  no included paper pair: INCONCLUSIVE\n"); fi;
'''
        return body + "QUIT;;\n"

    if method == "kb-fill-first-all":
        body = 'LoadPackage("kbmag");;\n'
        for i, filling in enumerate(data["fillings"]):
            relators = filling["relators"] + data["relators"]
            body += f"F := FreeGroup({data['ngens']});;\n"
            body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
            body += ("G := F/rels;;\n"
                     "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
                     "fg := FreeGeneratorsOfFpGroup(H);; "
                     "rl := RelatorsOfFpGroup(H);;\n")
            body += (f'Print("local case {i}: drift={filling["drift"]} '
                     f'signs=({filling["sign_a"]:+d},{filling["sign_b"]:+d}) ",'
                     'Length(fg)," gens/",Length(rl)," rels\\n");\n')
            body += r'''
if Length(fg)=0 then
  Print("  CERTIFIED TRIVIAL (Tietze)\n");
else
  rws := KBMAGRewritingSystem(H);;
  attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
  reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                     z -> ReducedForm(rws,z));;
  Print("  KB returned=",attempt," confluent=",IsConfluent(rws),
        " generator_normal_forms=",reductions,"\n");
  if ForAll(reductions,IsOne) then
    Print("  CERTIFIED TRIVIAL: every generator rewrites to identity\n");
  else Print("  INCONCLUSIVE\n"); fi;
fi;
'''
        return body + "QUIT;;\n"

    if method == "paper-kb-hard":
        def inv(word):
            return [-letter for letter in reversed(word)]

        tracked = data["tracked_words"]
        alpha_dir = tracked["geom_A"] + inv(tracked["geom_r"])
        beta_dir = (inv(tracked["geom_r"]) + tracked["geom_M"] +
                    tracked["geom_r"] + tracked["geom_B"])
        fills = [tracked["geom_M"] + alpha_dir,
                 tracked["geom_N"] + inv(beta_dir)]
        base = data["relators"]
        variants = [
            ("base_then_fill", base + fills),
            ("fill_then_base", fills + base),
            ("reverse_base", list(reversed(base)) + fills),
            ("short_first", sorted(base + fills, key=len)),
            ("long_first", sorted(base + fills, key=len, reverse=True)),
        ]
        body = 'LoadPackage("kbmag");;\ndone := false;;\n'
        for name, relators in variants:
            body += "if not done then\n"
            body += f"F := FreeGroup({data['ngens']});;\n"
            body += f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
            body += r'''G := F/rels;;
iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;
fg := FreeGeneratorsOfFpGroup(H);; rl := RelatorsOfFpGroup(H);;
'''
            body += (f'Print("hard variant {name}: ",Length(fg)," gens/",'
                     'Length(rl)," rels\\n");\n')
            body += r'''
if Length(fg)=0 then
  Print("  CERTIFIED TRIVIAL (Tietze)\n"); done := true;
else
  rws := KBMAGRewritingSystem(H);;
  attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
  reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                     z -> ReducedForm(rws,z));;
  Print("  KB returned=",attempt," confluent=",IsConfluent(rws),
        " generator_normal_forms=",reductions,"\n");
  if ForAll(reductions,IsOne) then
    Print("  CERTIFIED TRIVIAL: every generator rewrites to identity\n");
    done := true;
  else Print("  INCONCLUSIVE\n"); fi;
fi;
fi;
'''
        return body + "QUIT;;\n"

    if method == "paper-kb-all":
        def inv(word):
            return [-letter for letter in reversed(word)]

        def signed(word, sign):
            return word if sign > 0 else inv(word)

        tracked = data["tracked_words"]
        alpha_dirs = {
            "n0_Ax": tracked["geom_A"] + tracked["geom_x"],
            "n1_Arinv": tracked["geom_A"] + inv(tracked["geom_r"]),
        }
        beta_dir = (inv(tracked["geom_r"]) + tracked["geom_M"] +
                    tracked["geom_r"] + tracked["geom_B"])
        body = 'LoadPackage("kbmag");;\n'
        for alpha_name, alpha_dir in alpha_dirs.items():
            for sign_a in (1, -1):
                for sign_b in (1, -1):
                    filling_relators = [
                        tracked["geom_M"] + signed(alpha_dir, sign_a),
                        tracked["geom_N"] + signed(beta_dir, sign_b),
                    ]
                    relators = data["relators"] + filling_relators
                    body += f"F := FreeGroup({data['ngens']});;\n"
                    body += (f"rels := [{','.join(gap_word(r) for r in relators)}];;\n"
                             "G := F/rels;;\n"
                             "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
                             "fg := FreeGeneratorsOfFpGroup(H);; "
                             "rl := RelatorsOfFpGroup(H);;\n")
                    body += (f'Print("paper fillings {alpha_name} '
                             f'({sign_a:+d},{sign_b:+d}): ",'
                             'Length(fg)," gens/",Length(rl)," rels H1=",'
                             'AbelianInvariants(H),"\\n");\n')
                    body += r'''
if Length(fg)=0 then
  Print("  CERTIFIED TRIVIAL (Tietze)\n");
else
  rws := KBMAGRewritingSystem(H);;
  attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
  reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                     z -> ReducedForm(rws,z));;
  Print("  KB returned=",attempt," confluent=",IsConfluent(rws),
        " generator_normal_forms=",reductions,"\n");
  if ForAll(reductions,IsOne) then
    Print("  CERTIFIED TRIVIAL: every generator rewrites to identity\n");
  else
    Print("  INCONCLUSIVE\n");
  fi;
fi;
'''
        return body + "QUIT;;\n"

    if method == "word-all":
        selected = {name: word for name, word in data["tracked_words"].items()
                    if (name.startswith("table_") or
                        name.startswith("coord_alpha_base_") or
                        name.startswith("coord_beta_base_"))}

        def inv(word):
            return [-letter for letter in reversed(word)]

        def red(word):
            out = []
            for letter in word:
                if out and out[-1] == -letter:
                    out.pop()
                else:
                    out.append(letter)
            return out

        tracked = data["tracked_words"]
        A, s = tracked["geom_A"], tracked["geom_s"]
        N, y = tracked["geom_N"], tracked["geom_y"]
        # Directly test Wuebben's load-bearing drilled-fiber relation R3 in
        # the independently triangulated two-torus complement.  Earlier runs
        # checked the same transport in the unpunctured mapping cylinder and
        # compared only low-index fingerprints for the complement; neither is
        # an equality test in pi_1(C).  In the paper's coordinates:
        #
        #   B (s^-1 r^-1 y x) B^-1 = r^-1 s^-1 x.
        #
        # The tracked geom_* loops are all based in the actual complement, so
        # an identity reduction here would be a direct complement-level
        # algebraic certificate; a nonempty partial normal form is only
        # inconclusive unless the system is confluent.
        x, r, B = (tracked["geom_x"], tracked["geom_r"],
                   tracked["geom_B"])
        kappa3 = inv(s) + inv(r) + y + x
        psi_kappa3 = inv(r) + inv(s) + x
        selected["table_R3_complement"] = red(
            B + kappa3 + inv(B) + inv(psi_kappa3))
        # A genuine peripheral meridian/longitude pair lies in one boundary
        # three-torus and therefore commutes.  This is a necessary,
        # basing-sensitive diagnostic for the literal pairs used by the
        # direct fillings.
        for label, meridian, longitude in (
                ("alpha", tracked["geom_M"], tracked["lb_a_y1"]),
                ("beta", tracked["geom_N"], tracked["lb_b_s2"])):
            selected[f"peripheral_{label}_commutator"] = red(
                inv(meridian) + inv(longitude) + meridian + longitude)
        if "lb_a_y2" in tracked:
            r = tracked["geom_r"]
            adjacent = A + inv(r)
            for y_sign in (1, -1):
                yy = y if y_sign > 0 else inv(y)
                candidate = yy + adjacent + inv(yy)
                selected[f"scan_y2_Arinv_conj_y{y_sign:+d}"] = red(
                    inv(tracked["lb_a_y2"]) + candidate)
            if "geom_M_y2" in tracked:
                M, M_y2 = tracked["geom_M"], tracked["geom_M_y2"]
                for y_sign in (1, -1):
                    yy = y if y_sign > 0 else inv(y)
                    selected[f"scan_M_y2_conj_y{y_sign:+d}"] = red(
                        inv(M_y2) + yy + M + inv(yy))
                x, B = tracked["geom_x"], tracked["geom_B"]
                corr_y1 = inv(r) + M + r
                for m_sign in (1, -1):
                    mm = M_y2 if m_sign > 0 else inv(M_y2)
                    corr_y2 = x + mm + inv(x)
                    selected[f"scan_beta_correction_y2_M{m_sign:+d}"] = red(
                        inv(corr_y1) + corr_y2)
                    if "lb_b_s2" in tracked:
                        selected[f"scan_beta_base_y2_M{m_sign:+d}"] = red(
                            inv(tracked["lb_b_s2"]) + corr_y2 + B)
        for a_sign in (1, -1):
            aa = A if a_sign > 0 else inv(A)
            lhs = aa + s + inv(aa)
            for n_sign in (1, -1):
                nn = N if n_sign > 0 else inv(N)
                for placement in ("left", "right"):
                    rhs = nn + y if placement == "left" else y + nn
                    name = (f"scan_M1_A{a_sign:+d}_N{n_sign:+d}_"
                            f"{placement}")
                    selected[name] = red(lhs + inv(rhs))
        corrected = tracked.get("alpha_s_corrected_boundary")
        if corrected is not None:
            lhs = A + s + inv(A)
            for cycle_sign in (1, -1):
                cc = corrected if cycle_sign > 0 else inv(corrected)
                selected[f"scan_alpha_cycle_{cycle_sign:+d}_vs_y"] = \
                    red(cc + inv(y))
                for n_sign in (1, -1):
                    nn = N if n_sign > 0 else inv(N)
                    for placement in ("left", "right"):
                        target = nn + lhs if placement == "left" else lhs + nn
                        name = (f"scan_alpha_cycle_{cycle_sign:+d}_N"
                                f"{n_sign:+d}_{placement}")
                        selected[name] = red(cc + inv(target))
            # The grid meridian is based at the source-side corner.  The
            # Table 1 word AsA^-1 starts at the opposite corner, so its plain
            # correction is the transported inverse A*Ngrid^-1*A^-1.
            grid_n = tracked["alpha_s_grid_N"]
            paper_n = A + inv(grid_n) + inv(A)
            selected["scan_M1_transported_Npaper"] = red(
                A + s + inv(A) + inv(paper_n + y))
        names = sorted(selected)
        body = 'LoadPackage("kbmag");;\n'
        body += f"F := FreeGroup({data['ngens']});;\n"
        body += f"rels := [{','.join(gap_word(r) for r in data['relators'])}];;\n"
        body += "G := F/rels;;\n"
        body += "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
        body += ("hom := GroupHomomorphismByImages(F,G,GeneratorsOfGroup(F),"
                 "GeneratorsOfGroup(G));;\n")
        body += "names := [" + ",".join(f'\"{name}\"' for name in names) + "];;\n"
        body += "wFs := [" + ",".join(
            gap_word(selected[name]) for name in names) + "];;\n"
        body += r'''
wHs := List(wFs,w->Image(iso,Image(hom,w)));;
rws := KBMAGRewritingSystem(H);;
attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
freegens := GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws));;
tofree := function(w) local letters;
  letters := LetterRepAssocWord(UnderlyingElement(w));
  if Length(letters)=0 then return One(freegens[1]); fi;
  return Product(letters,i->freegens[AbsInt(i)]^SignInt(i));
end;;
normals := List(wHs,w->ReducedForm(rws,tofree(w)));;
Print("KB returned=",attempt," confluent=",IsConfluent(rws),"\n");
for i in [1..Length(names)] do
  Print(names[i],": ",normals[i]);
  if IsOne(normals[i]) then Print("  CERTIFIED IDENTITY\n");
  else Print("  INCONCLUSIVE\n"); fi;
od;
probeNames := ["peripheral_alpha_commutator",
               "peripheral_beta_commutator",
               "table_R3_complement"];;
for p in [2,3,5] do
  attemptP := CALL_WITH_CATCH(EpimorphismPGroup,[H,p,6]);;
  if attemptP[1] <> true then
    Print("p=",p," class=6 quotient: computation failed\n");
  else
    epiP := attemptP[2];; QP := Image(epiP);;
    Print("p=",p," class=6 quotient order=",Size(QP),"\n");
    for probeName in probeNames do
      probeIndex := Position(names,probeName);;
      probeImage := Image(epiP,wHs[probeIndex]);;
      Print("  ",probeName,": ");
      if IsOne(probeImage) then Print("identity\n");
      else Print("NONTRIVIAL\n"); fi;
    od;
  fi;
od;
QUIT;;
'''
        return body

    if method == "word":
        assert word_name in data["tracked_words"], \
            f"unknown tracked word {word_name!r}"
        word = data["tracked_words"][word_name]
        body = 'LoadPackage("kbmag");;\n'
        body += f"F := FreeGroup({data['ngens']});;\n"
        body += f"rels := [{','.join(gap_word(r) for r in data['relators'])}];;\n"
        body += "G := F/rels;;\n"
        body += "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;\n"
        body += ("hom := GroupHomomorphismByImages(F,G,GeneratorsOfGroup(F),"
                 "GeneratorsOfGroup(G));;\n")
        body += f"wF := {gap_word(word)};; wH := Image(iso,Image(hom,wF));;\n"
        body += f'Print("word {word_name}: simplified image=",wH,"\\n");\n'
        body += r'''
rws := KBMAGRewritingSystem(H);;
attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
freegens := GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws));;
letters := LetterRepAssocWord(UnderlyingElement(wH));;
if Length(letters)=0 then wf := One(freegens[1]);
else wf := Product(letters,i->freegens[AbsInt(i)]^SignInt(i)); fi;;
normal := ReducedForm(rws,wf);;
Print("  KB returned=",attempt," confluent=",IsConfluent(rws),
      " normal_form=",normal,"\n");
if IsOne(normal) then
  Print("  CERTIFIED IDENTITY: the tracked word rewrites to one\n");
else
  Print("  INCONCLUSIVE\n");
fi;
QUIT;;
'''
        return body

    if method == "summary":
        body = ""
        for i in range(len(data["fillings"])):
            body += case_setup(data, i)
        return body + "QUIT;;\n"

    if method == "kb-all":
        body = 'LoadPackage("kbmag");;\n'
        for i in range(len(data["fillings"])):
            body += case_setup(data, i)
            body += r'''
rws := KBMAGRewritingSystem(H);;
attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                   z -> ReducedForm(rws,z));;
Print("  KB returned=",attempt," confluent=",IsConfluent(rws),
      " generator_normal_forms=",reductions,"\n");
if ForAll(reductions,IsOne) then
  Print("  CERTIFIED TRIVIAL: every generator rewrites to identity\n");
else
  Print("  INCONCLUSIVE\n");
fi;
'''
        return body + "QUIT;;\n"

    if method == "gap-export-all":
        body = ('out := OutputTextFile("r_gap_simplified.json",false);;\n'
                'SetPrintFormattingStatus(out,false);; PrintTo(out,"{\\"format\\":'
                '\\"gap-simplified-v1\\",\\"cases\\":[");;\n')
        for i in range(len(data["fillings"])):
            if i:
                body += 'PrintTo(out,",");;\n'
            body += case_setup(data, i)
            body += (f'PrintTo(out,"{{\\"case\\":{i},\\"ngens\\":",Length(fg),'
                     '" ,\\"extrep_relators\\":",List(rl,ExtRepOfObj),"}");;\n')
        body += ('PrintTo(out,"]}\\n");; CloseStream(out);;\n'
                 'Print("wrote r_gap_simplified.json\\n"); QUIT;;\n')
        return body

    body = case_setup(data, case)
    if method == "kb":
        body = 'LoadPackage("kbmag");;\n' + body + r'''
rws := KBMAGRewritingSystem(H);;
attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
Print("  KnuthBendix returned=",attempt," confluent=",IsConfluent(rws),"\n");
reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                   z -> ReducedForm(rws,z));;
Print("  generator normal forms=",reductions,"\n");
if ForAll(reductions,IsOne) then
  Print("  CERTIFIED TRIVIAL: every generator rewrites to identity\n");
elif IsConfluent(rws) then
  Print("  completed system size=",Size(rws),"\n");
else
  Print("  INCONCLUSIVE\n");
fi;
QUIT;;
'''
    elif method == "automatic":
        body = 'LoadPackage("kbmag");;\n' + body + r'''
rws := KBMAGRewritingSystem(H);;
attempt := CALL_WITH_CATCH(AutomaticStructure,[rws,true]);;
Print("  AutomaticStructure returned=",attempt,"\n");
if attempt=[true,true] then
  reductions := List(GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws)),
                     z -> ReducedForm(rws,z));;
  Print("  generator normal forms=",reductions," size=",Size(rws),"\n");
fi;
QUIT;;
'''
    elif method == "ace":
        body = 'LoadPackage("ace");;\n' + body + f'''
for subgroup in Concatenation(List(fg,z->[z]),[[]]) do
  stats := ACEStats(fg,rl,subgroup : hard, workspace := {workspace});;
  Print("  ACE subgroup_generators=",Length(subgroup)," index=",stats.index,
        " total_cosets=",stats.totcosets,"\\n");
od;
QUIT;;
'''
    elif method == "quotients":
        body += r'''
targets := [AlternatingGroup(5),PSL(2,7),AlternatingGroup(6),PSL(2,8)];;
for target in targets do
  epis := GQuotients(H,target);;
  Print("  quotient target order=",Size(target)," epimorphisms=",Length(epis),"\n");
od;
subs := LowIndexSubgroupsFpGroup(H,10);;
Print("  subgroup indices <=10: ",List(subs,u->Index(H,u)),"\n");
QUIT;;
'''
    elif method == "gap-export":
        body += r'''
Print("  extrep_relators=",List(rl,ExtRepOfObj),"\n");
QUIT;;
'''
    else:
        raise ValueError(method)
    return body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("method", choices=("summary", "kb", "kb-all", "automatic",
                                           "ace", "quotients", "gap-export",
                                           "gap-export-all", "word", "word-all",
                                           "paper-kb-all", "paper-kb-hard",
                                           "kb-fill-first-all",
                                           "local-paper-inclusion-all",
                                           "direct-paper-kb-all",
                                           "direct-paper-kb-hard",
                                           "direct-paper-export",
                                           "direct-paper-replay"))
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--workspace", type=int, default=25_000_000)
    parser.add_argument("--input", default="r_presentations.json")
    parser.add_argument("--gap-file", default="r_group_attack.g")
    parser.add_argument("--name", help="tracked word name for the word method")
    parser.add_argument("--timeout", type=int, default=14_000)
    parser.add_argument("--gap", default="gap",
                        help="GAP executable (default: gap from PATH)")
    parser.add_argument("--write-only", action="store_true")
    args = parser.parse_args()
    data = load_presentations(args.input)
    assert 0 <= args.case < len(data["fillings"])
    program = gap_program(data, args.method, args.case, args.workspace, args.name)
    with open(args.gap_file, "w", encoding="ascii") as stream:
        stream.write(program)
    if args.write_only:
        print(f"wrote {args.gap_file}")
        return
    if args.method == "direct-paper-replay":
        with open("direct_rws/manifest.json", encoding="ascii") as stream:
            saved_manifest = json.load(stream)
        assert saved_manifest["format"] == "luttinger-direct-rws-export-v1"
        def replay_sha256(path):
            digest = hashlib.sha256()
            with open(path, "rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()

        assert replay_sha256(saved_manifest["input"]) == \
            saved_manifest["input_sha256"], "input presentation digest mismatch"
        assert replay_sha256(saved_manifest["gap_program"]) == \
            saved_manifest["gap_program_sha256"], "export program digest mismatch"
        for name, expected in saved_manifest["artifacts_sha256"].items():
            assert replay_sha256(os.path.join("direct_rws", name)) == expected, \
                f"digest mismatch: {name}"
        print("verified input and export-program digests plus "
              f"{len(saved_manifest['artifacts_sha256'])} artifact digests")
    if args.method == "direct-paper-export":
        os.makedirs("direct_rws", exist_ok=True)
    result = subprocess.run([args.gap, "-q", args.gap_file], capture_output=True,
                            text=True, timeout=args.timeout)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    expected_marker = {
        "direct-paper-export": "ALL EIGHT EXPORTS CERTIFIED",
        "direct-paper-replay": "ALL EIGHT EXPORTED SYSTEMS REPLAYED",
    }.get(args.method)
    marker_missing = expected_marker is not None and expected_marker not in result.stdout
    if marker_missing:
        print(f"ERROR: GAP did not emit required marker: {expected_marker}")
    if result.returncode == 0 and not marker_missing and args.method == "direct-paper-export":
        def sha256(path):
            digest = hashlib.sha256()
            with open(path, "rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()

        artifacts = {}
        for name in sorted(os.listdir("direct_rws")):
            path = os.path.join("direct_rws", name)
            if os.path.isfile(path) and name != "manifest.json":
                artifacts[name] = sha256(path)
        cases = []
        for filling in data["paper_fillings"]:
            hard = (filling["half_drift"] == "n0_y1" and
                    filling["sign_a"] == 1 and filling["sign_b"] == 1)
            cases.append({
                "half_drift": filling["half_drift"],
                "sign_a": filling["sign_a"],
                "sign_b": filling["sign_b"],
                "relator_order": "base_then_fill" if hard else "fill_then_base",
            })
        manifest = {
            "format": "luttinger-direct-rws-export-v1",
            "input": args.input,
            "input_sha256": sha256(args.input),
            "gap_program": args.gap_file,
            "gap_program_sha256": sha256(args.gap_file),
            "cases": cases,
            "artifacts_sha256": artifacts,
        }
        with open("direct_rws/manifest.json", "w", encoding="ascii") as stream:
            json.dump(manifest, stream, indent=2, sort_keys=True)
            stream.write("\n")
        print("wrote direct_rws/manifest.json with "
              f"{len(artifacts)} hashed artifacts")
    raise SystemExit(result.returncode if not marker_missing else 1)


if __name__ == "__main__":
    main()
