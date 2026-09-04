# Witness search on the displayed relation sheet (Run 72 scripts, issue #800)

A search for a unit-slope neighbour of the displayed relation sheet whose filled group is provably nontrivial. None was
found; every neighbour is trivial. The last cell to close, the `(+,+)` sheet
with alpha shift `n = -1` and beta shift `m = +1` (case 9), needed a coset
table of 39,024,955 rows and closed on 3 September 2026 in a 4 GB ACE
workspace, reproducing the unlogged scratch run that Run 77 reported.

## Read this first: what these groups are

`common.g` builds Wuebben's current-coordinate family exactly as his
`decide2.g` defines it (vendored and hash-checked under
`../wuebben_dictionary/wuebben_anc/`). At `(m,n) = (0,0)`, `e3=+1, e4=-1,
e5=-1` this is the paper's displayed ten-relation sheet (Run 71). The base
relations include the printed x-transport row `B x B^-1 = y^-1`. For the
audit loops that row is certified only as `B x B^-1 = y^-1 M`, with `M`
undecided in the complement (#818, `../honest_filling/README.md`). So:

* every collapse in this directory is a collapse of the *displayed sheet*,
  not of a group derived from the audit complex;
* the negative result (no nontrivial neighbour) is likewise a statement
  about the displayed sheet and its neighbours.

Nothing here bears on whether `pi_1(V_aud) = 1` until the printed row is
certified or replaced by the certified one.

## Insertion convention (the caveat of #800 made a specification)

With `dirTaBase = A x`, `dirTaFib = (r x)^-1`, `dirTbBase = r^-1 M^-e5 r B`,
`dirTbFib = s r^-1 s^-1`, the fillings are

    alpha:  M . ( dirTaBase . dirTaFib^n )^eA
    beta:   N . ( dirTbBase . dirTbFib^m )^eB

The fiber-direction shift is appended to the longitude word, inside the
sign exponent. `n` shifts the alpha filling, `m` the beta filling.

## Cases

Twelve "ours" cases: the paper's signs `e3=+1, e4=-1, e5=-1`, alpha shift
`n = -1` (the column where Wuebben's own `decide2` log overflows for every
sign system), beta shift `m in {-1, 0, 1}`, all four `(eA, eB)`.

| case | m | (eA, eB) | stage 1, 4,000,000 fixed | stage 1b, 16,000,000 fixed | stage 1c, GAP Size ladder to 32,000,000 |
|---|---|---|---|---|---|
| 1 | -1 | (+,+) | overflow, 2 s | not run | classic enumerator overflows 32M (`grid_3x3.g`); **trivial by ACE hard**, peak 10.5M cosets (`grid_cell_ace_n-1_m-1.log`) |
| 2 | -1 | (+,-) | overflow | overflow, 15 s | trivial, 170 s |
| 3 | -1 | (-,+) | overflow | trivial, 31 s | trivial, 47 s |
| 4 | -1 | (-,-) | overflow | trivial, 30 s | trivial, 44 s |
| 5 | 0 | (+,+) | overflow | not run | classic enumerator overflows 32M (`grid_3x3.g`); **trivial by ACE hard**, peak 11.8M cosets (`grid_cell_ace_n-1_m0.log`) |
| 6 | 0 | (+,-) | overflow | overflow, 15 s | trivial, 143 s |
| 7 | 0 | (-,+) | overflow | overflow, 16 s | trivial, 178 s |
| 8 | 0 | (-,-) | overflow | overflow, 16 s | trivial, 50 s |
| 9 | 1 | (+,+) | overflow | not run | classic enumerator overflows 32M; ACE hard/felsch/sims9 fill a 1.9 GB workspace at ~29.6M cosets; **trivial by ACE hard** in a 4 GB workspace, peak 39,024,955 cosets (`grid_cell_ace_n-1_m1_big.log`); `runs/77` reports 588 s from an unlogged scratch run |
| 10 | 1 | (+,-) | overflow | overflow, 15 s | trivial, 231 s |
| 11 | 1 | (-,+) | overflow | overflow, 15 s | trivial, 118 s |
| 12 | 1 | (-,-) | overflow | overflow, 15 s | trivial, 106 s |

`H_1 = 0` in every case (stage 1). Twelve further "wuebben" cases (his four
sign patterns, `m in {-1,0,1}`) are defined in `common.g` but were never
run; `stage1.log` stops after case 12.

The lesson of the three columns is the one Run 77 drew: a fixed coset
ceiling of 4,000,000 or 16,000,000 overflows in seconds on groups that GAP's
retry ladder then finishes in minutes. "Does not terminate at N cosets" is a
table-size artifact, not evidence of nontriviality.

## Stage 2: finite quotients and low-index subgroups of case 9

Before its collapse was known, case 9 was run against every nonabelian
simple group of order below 100,000 (`GQuotients`, mirroring Wuebben's
`phase3_worker.g` including its excluded-orders pre-mark) and
`LowIndexSubgroupsFpGroup` to index 7. Results in `logs/case9_*.log`:
no quotient onto any of the 30 targets that finished (A5 through L2(53),
0.2 s to 5,013 s each); the M12 job did not finish; low-index to 7 finds only
the whole group. So case 9, now known trivial, had no nontrivial finite quotient of order below 100,000 and no proper
subgroup of index at most 7, as it must: consistent with trivial, and not a witness.

## The 3x3 grid on the (+,+) sheet

`grid_3x3.g` runs all nine `(n, m) in {-1,0,1}^2` cells of the displayed
`(+,+)` sheet through fixed coset ceilings of 4,000,000, 16,000,000 and
32,000,000 (GAP's classic enumerator, silent fail on overflow), recording
`H_1`, the order and the time per cell (`logs/grid_3x3.log`, 2026-09-03).
The three cells that overflow were then run through ACE 5.3 (GAP package in
the `luttinger-kbmag-proof:local` image) with `grid_cell_ace.g`, workspace
480,000,000 words (1.9 GB, about 40,000,000 cosets), strategies `hard`,
`felsch`, `sims := 9` (`logs/grid_cell_ace_*.log`). After the Docker VM was
enlarged from 3.8 GB to 8 GB, the one cell still open was rerun with
workspace 1,000,000,000 words (4 GB, about 83,000,000 cosets), strategy
`hard` (`logs/grid_cell_ace_n-1_m1_big.log`, 3 September 2026).

| n \ m | -1 | 0 | +1 |
|---|---|---|---|
| -1 | GAP overflow at 32M; **trivial by ACE hard**, peak 10,486,381 cosets | GAP overflow at 32M; **trivial by ACE hard**, peak 11,774,905 cosets | GAP overflow at 32M; ACE hard, felsch, sims9 all fill 1.9 GB at ~29.6M cosets; **trivial by ACE hard** in 4 GB, peak 39,024,955 cosets |
| 0 | trivial, < 1 s | trivial, < 1 s (the displayed sheet) | trivial, < 1 s |
| +1 | trivial, < 1 s | trivial, < 1 s | trivial, < 1 s |

`H_1 = 0` in all nine cells. All nine are trivial. The `(-1,+1)` cell is the
expensive one: its table peaks at 39,024,955 cosets, above what the 1.9 GB
ACE workspace holds (it filled at about 29.6M) and above native GAP's 6 GB
cap (reached before 48,000,000 cosets in the classic enumerator); in the 4 GB
ACE workspace it closes in 44 s of wall time (container start to exit).

**What this says about Run 77.** `runs/77` reports these three cells trivial
from scratch runs that were not kept: `(-1,-1)` 123 s, `(-1,0)` 89 s,
`(-1,+1)` 588 s, "after GAP raised the table limit past 4,000,000". All
three are now reproduced in-repo, by a different enumerator: the fixed
ceilings of GAP's classic enumerator were the wrong tool, and ACE's
Felsch-heavy strategy closes two of them at 10--12 million cosets and the
third at 39 million. Run 77's sentence "every shifted unit-slope filling
enumerated to completion is trivial" is therefore supported for all nine
cells. Its other claim, that "does not terminate at N cosets" is a
table-size or strategy artifact rather than evidence of nontriviality, is
reinforced: the reviewer's own example `(-1,-1)` collapses.

## Files

| file | what |
|---|---|
| `common.g` | the family, the 24 cases, the target list, helpers |
| `stage1_enumerate.g`, `stage1.log` | fixed 4,000,000-coset enumeration, `H_1`, all cases |
| `stage1b_enumerate.g`, `logs/stage1b_*.log` | fixed 16,000,000-coset enumeration |
| `stage1c_size.g`, `run_stage1c.sh`, `logs/stage1c_*.log` | GAP Size ladder to 32,000,000, one case per process |
| `stage2_worker.g`, `run_stage2.sh`, `logs/case9_*.log` | quotient and low-index search, one (case, target) per process |
| `grid_3x3.g`, `logs/grid_3x3.log` | the nine-cell shift grid on the (+,+) sheet, fixed ceilings to 32M |
| `grid_cell_big.g`, `logs/grid_cell_n-1_m0_48M.log` | one cell at one larger native ceiling (hit the 6 GB memory cap) |
| `grid_cell_ace.g`, `logs/grid_cell_ace_*.log` | one cell through ACE (docker image), strategy hard / felsch / sims9, 1.9 GB workspace |
| `logs/grid_cell_ace_n-1_m1_big.log` | the `(-1,+1)` cell through ACE hard with a 4 GB workspace: trivial, peak 39,024,955 cosets |

GAP 4.16.1, native (`~/opt/gap-4.16.1/gap -q -A`).
