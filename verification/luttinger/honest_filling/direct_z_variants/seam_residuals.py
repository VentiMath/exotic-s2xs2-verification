"""Print the seam-consistency residuals in sheet letters and check the hand derivation
   residual(A^-1B^-1AB, r) = r A^-1 N^-1 A r^-1  (trivial iff N = 1 in the filled group)."""
_src = open('../wuebben_dictionary/reduce_in_halted.py').read()
exec(_src[:_src.index('sealed = json.load')])
exec(open('seam_consistency.py').read().split("sysfile =")[0].split("exec(_src")[1].split("\n",1)[1])
L = {1:'x',2:'y',3:'r',4:'s',5:'A',6:'B',7:'M',8:'N'}
def show(w): return ' '.join(L[abs(l)] + ('' if l>0 else '^-1') for l in w) or '1'
def from_kb(w): return [ (l+1)//2 if l%2 else -(l//2) for l in w]
eqs = load('../kbmag/honest_y1_p1_p1.rws.kbprog'); Rw = RWS(eqs)
def nf(w): return from_kb(Rw.reduce(to_kb(freered(w)))[0])
for name, d in arr.items():
    for g in (X,Y,R,S):
        w = freered(d + [g] + inv(d) + inv(h_of(d, g)))
        n = nf(w)
        if n: print(f'{name} g={L[g]}: delta g delta^-1 = {show(h_of(d,g))} * [{show(n)}]')
print('--- hand check for A^-1B^-1AB, g=r: residual should equal r A^-1 N^-1 A r^-1')
d = arr['AiBiAB']; w = freered(d + [R] + inv(d) + inv(h_of(d, R)))
hand = [R, -A, -N, A, -R]
print('residual nf      :', show(nf(w)))
print('hand word nf     :', show(nf(hand)))
print('difference nf    :', show(nf(list(w) + inv(hand))), '(empty = certified equal)')
print('N nf             :', show(nf([N])), '   A^-1 N A nf:', show(nf([-A,N,A])), '   M nf:', show(nf([M])))
