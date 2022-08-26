-- Just for fun, a solution taking advantage of Haskell not caring what order
-- you declare variables in (since they can never be reassigned).
--
-- I used Vim to edit the puzzle input and turn it into Haskell syntax. Doing
-- this for other puzzle inputs is an exercise left to the reader ;)

import Data.Bits ((.&.), (.|.), shift)
import qualified Data.Bits (complement)


main = print a'

rshift a b = shift a (-b)

complement :: Int -> Int
complement = Data.Bits.complement

dr' = complement dq'
kh' = kg' .|. kf'
eq' = ep' .|. eo'
b' = 44430
gt' = complement gs'
dp' = dd' .|. do'
ej' = eg' .&. ei'
ag' = y' .&. ae'
ka' = jx' .&. jz'
lg' = lf' `rshift` 2
ac' = z' .&. aa'
el' = dy' .&. ej'
bk' = bj' .|. bi'
km' = kk' `rshift` 3
co' = complement cn'
gq' = gn' .&. gp'
ct' = cq' .&. cs'
es' = eo' `shift` 15
ln' = lg' .|. lm'
ek' = dy' .|. ej'
dj' = complement di'
fj' = 1 .&. fi'
kj' = kf' `shift` 15
jz' = complement jy'
fu' = complement ft'
fv' = fs' .&. fu'
hs' = complement hr'
cm' = ck' .|. cl'
js' = jp' `rshift` 5
jc' = iv' .|. jb'
iu' = is' .|. it'
lf' = ld' .|. le'
fd' = complement fc'
dn' = complement dm'
bz' = bn' .|. by'
am' = aj' .&. al'
ch' = cd' `shift` 15
kc' = jp' .&. ka'
cu' = ci' .|. ct'
gy' = gv' .&. gx'
dm' = de' .&. dk'
aa' = x' `rshift` 5
eu' = et' `rshift` 2
aq' = x' `rshift` 1
ih' = ia' .|. ig'
ce' = bk' `shift` 1
af' = y' .|. ae'
cb' = complement ca'
h' = e' .&. f'
ii' = ia' .&. ig'
cn' = ck' .&. cl'
ji' = complement jh'
ab' = z' .|. aa'
eo' = 1 .&. en'
ie' = ib' .&. ic'
ei' = complement eh'
jb' = iy' .&. ja'
bc' = complement bb'
hb' = ha' .|. gz'
cy' = 1 .&. cx'
ay' = complement ax'
ex' = ev' .|. ew'
bo' = bn' `rshift` 2
et' = er' .|. es'
fb' = eu' .|. fa'
kb' = jp' .|. ka'
ed' = ea' .&. eb'
n' = k' .&. m'
ev' = et' `rshift` 3
ew' = et' `rshift` 5
is' = hz' `rshift` 1
kk' = ki' .|. kj'
i' = complement h'
lz' = lv' `shift` 15
bl' = as' `rshift` 1
hy' = hu' `shift` 15
iz' = iw' .&. ix'
ly' = lf' `rshift` 1
fw' = fp' .|. fv'
an' = 1 .&. am'
bj' = ap' `shift` 1
ao' = u' `shift` 1
f' = b' `rshift` 5
jy' = jq' .&. jw'
iw' = iu' `rshift` 3
ik' = ih' .&. ij'
ja' = complement iz'
dl' = de' .|. dk'
jg' = iu' .|. jf'
bf' = as' .&. bd'
e' = b' `rshift` 3
jx' = jq' .|. jw'
jd' = iv' .&. jb'
ci' = cg' .|. ch'
jh' = iu' .&. jf'
a' = lx'
cd' = 1 .&. cc'
ma' = ly' .|. lz'
em' = complement el'
bi' = 1 .&. bh'
fe' = fb' .&. fd'
lr' = lf' .|. lq'
bp' = bn' `rshift` 3
ca' = bn' .&. by'
ai' = af' .&. ah'
cz' = cf' `shift` 1
dy' = dw' .|. dx'
gw' = gj' .&. gu'
jj' = jg' .&. ji'
jt' = jr' .|. js'
bn' = bl' .|. bm'
gk' = gj' `rshift` 2
cq' = cj' .|. cp'
gv' = gj' .|. gu'
o' = b' .|. n'
r' = o' .&. q'
bm' = bi' `shift` 15
er' = dy' `rshift` 1
cx' = cu' .&. cw'
iy' = iw' .|. ix'
he' = hc' .|. hd'
c' = 0
dd' = db' .|. dc'
kl' = kk' `rshift` 2
fk' = eq' `shift` 1
eg' = dz' .|. ef'
ee' = complement ed'
lx' = lw' .|. lv'
fz' = fw' .&. fy'
eh' = dz' .&. ef'
jr' = jp' `rshift` 3
lo' = lg' .&. lm'
cj' = ci' `rshift` 2
bh' = be' .&. bg'
lw' = lc' `shift` 1
hp' = hm' .&. ho'
ju' = jr' .&. js'
ip' = 1 .&. io'
cp' = cm' .&. co'
id' = ib' .|. ic'
bg' = complement bf'
fr' = fo' `rshift` 5
it' = ip' `shift` 15
jw' = jt' .&. jv'
jf' = jc' .&. je'
dv' = du' .|. dt'
fy' = complement fx'
az' = aw' .&. ay'
gi' = ge' `shift` 15
al' = complement ak'
fo' = fm' .|. fn'
fi' = ff' .&. fh'
cl' = ci' `rshift` 5
da' = cz' .|. cy'
ez' = complement ey'
jv' = complement ju'
lt' = complement ls'
kx' = kk' .&. kv'
ij' = complement ii'
kt' = kl' .&. kr'
jo' = jk' `shift` 15
g' = e' .|. f'
bt' = complement bs'
hl' = hi' .&. hk'
il' = hz' .|. ik'
en' = ek' .&. em'
ap' = ao' .|. an'
ep' = dv' `shift` 1
ar' = an' `shift` 15
gh' = fo' `rshift` 1
in' = complement im'
ld' = kk' `rshift` 1
iq' = hw' `shift` 1
ef' = ec' .&. ee'
hv' = hb' `shift` 1
ke' = kb' .&. kd'
ak' = x' .&. ai'
dq' = dd' .&. do'
as' = aq' .|. ar'
ir' = iq' .|. ip'
do' = dl' .&. dn'
ix' = iu' `rshift` 5
be' = as' .|. bd'
gp' = complement go'
fl' = fk' .|. fj'
kg' = jm' `shift` 1
cw' = complement cv'
ds' = dp' .&. dr'
dx' = dt' `shift` 15
fm' = et' `rshift` 1
ea' = dy' `rshift` 3
fx' = fp' .&. fv'
q' = complement p'
de' = dd' `rshift` 2
fc' = eu' .&. fa'
bd' = ba' .&. bc'
dk' = dh' .&. dj'
lu' = lr' .&. lt'
hx' = he' `rshift` 1
fa' = ex' .&. ez'
dh' = df' .|. dg'
fn' = fj' `shift` 15
ky' = complement kx'
gr' = gk' .|. gq'
dz' = dy' `rshift` 2
gj' = gh' .|. gi'
lm' = lj' .&. ll'
aj' = x' .|. ai'
cc' = bz' .&. cb'
lv' = 1 .&. lu'
au' = as' `rshift` 3
cf' = ce' .|. cd'
io' = il' .&. in'
dw' = dd' `rshift` 1
lp' = complement lo'
t' = c' `shift` 1
df' = dd' `rshift` 3
dg' = dd' `rshift` 5
lk' = lh' .&. li'
li' = lf' `rshift` 5
eb' = dy' `rshift` 5
ku' = complement kt'
ba' = at' .|. az'
z' = x' `rshift` 3
ll' = complement lk'
lc' = lb' .|. la'
s' = 1 .&. r'
lj' = lh' .|. li'
lq' = ln' .&. lp'
kn' = kk' `rshift` 5
ec' = ea' .|. eb'
cv' = ci' .&. ct'
d' = b' `rshift` 2
ki' = jp' `rshift` 1
cs' = complement cr'
je' = complement jd'
jq' = jp' `rshift` 2
jp' = jn' .|. jo'
lh' = lf' `rshift` 3
dt' = 1 .&. ds'
ls' = lf' .&. lq'
le' = la' `shift` 15
fh' = complement fg'
bb' = at' .&. az'
ax' = au' .&. av'
kz' = kw' .&. ky'
x' = v' .|. w'
kw' = kk' .|. kv'
kv' = ks' .&. ku'
lb' = kh' `shift` 1
la' = 1 .&. kz'
kd' = complement kc'
y' = x' `rshift` 2
ff' = et' .|. fe'
fg' = et' .&. fe'
ad' = complement ac'
jm' = jl' .|. jk'
jk' = 1 .&. jj'
cg' = bn' `rshift` 1
kq' = complement kp'
ck' = ci' `rshift` 3
ey' = ev' .&. ew'
kf' = 1 .&. ke'
cr' = cj' .&. cp'
jl' = ir' `shift` 1
gx' = complement gw'
at' = as' `rshift` 2
jn' = iu' `rshift` 1
dc' = cy' `shift` 15
hi' = hg' .|. hh'
db' = ci' `rshift` 1
aw' = au' .|. av'
kp' = km' .&. kn'
hc' = gj' `rshift` 1
iv' = iu' `rshift` 2
ae' = ab' .&. ad'
du' = da' `shift` 1
bx' = complement bw'
ko' = km' .|. kn'
kr' = ko' .&. kq'
by' = bv' .&. bx'
ks' = kl' .|. kr'
hu' = 1 .&. ht'
di' = df' .&. dg'
ah' = complement ag'
k' = d' .|. j'
l' = d' .&. j'
p' = b' .&. n'
gg' = gf' .|. ge'
ha' = gg' `shift` 1
bq' = bn' `rshift` 5
bv' = bo' .|. bu'
gz' = 1 .&. gy'
w' = s' `shift` 15
if' = complement ie'
av' = as' `rshift` 5
bw' = bo' .&. bu'
im' = hz' .&. ik'
bs' = bp' .&. bq'
v' = b' `rshift` 1
m' = complement l'
br' = bp' .|. bq'
j' = g' .&. i'
bu' = br' .&. bt'
u' = t' .|. s'
ic' = hz' `rshift` 5
gs' = gk' .&. gq'
gf' = fl' `shift` 1
hg' = he' `rshift` 3
hd' = gz' `shift` 15
hm' = hf' .|. hl'
ge' = 1 .&. gd'
ga' = fo' .|. fz'
ig' = id' .&. if'
gb' = fo' .&. fz'
gu' = gr' .&. gt'
hq' = he' .|. hp'
ft' = fq' .&. fr'
gd' = ga' .&. gc'
fp' = fo' `rshift` 2
gn' = gl' .|. gm'
hj' = hg' .&. hh'
ho' = complement hn'
go' = gl' .&. gm'
hh' = he' `rshift` 5
gc' = complement gb'
ht' = hq' .&. hs'
ib' = hz' `rshift` 3
ia' = hz' `rshift` 2
fs' = fq' .|. fr'
hz' = hx' .|. hy'
hr' = he' .&. hp'
gm' = gj' `rshift` 5
hn' = hf' .&. hl'
hw' = hv' .|. hu'
hk' = complement hj'
gl' = gj' `rshift` 3
fq' = fo' `rshift` 3
hf' = he' `rshift` 2
