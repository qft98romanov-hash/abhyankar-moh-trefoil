-- Consolidated verification copy, 28 October 2026.
-- Exact source statements are unchanged; original logs are historical evidence.
-- This interpreter is optional and is not required by the Python certificate suite.
-- Exact certificates for the Shastri trefoil and harmonic figure-eight.
-- Mathematical constructions: Ivan Dorofeev, 24 October 2026.
-- Run from this directory: M2 --script verify_rectification.m2
-- No Python or SymPy is called. All computations use exact coefficients.
-- K = QQ[a]/(a^2-a+1) is a field: the discriminant is -3.
-- toField declares this already justified fact; it does not prove it.
-- The ring-map helper at performs simultaneous substitution.
-- exactDivX checks its remainder and keeps the quotient in P.
-- Inverse identities follow from the checked certificates, cancellation in
-- the integral domain P, and its injective localization P -> P[x^(-1)].
-- No argument from a nonzero Jacobian alone is used.
-- See README.md for the precise proof and scope. The script does not read TeX.


print "Macaulay2 exact rectification certificates";
print ("Macaulay2 version: " | toString version#"VERSION");

K = toField(QQ[a]/ideal(a^2-a+1));
P = K[x,y,z,t, MonomialOrder => GRevLex];

at = (p,xx,yy,zz,tt) -> (map(P,P,{xx,yy,zz,tt})) p;
certCheck = (label, p) -> (
    if p != 0 then error ("FAIL: " | label);
    print ("PASS: " | label);
    );
certList = (label, diffs) -> (
    scan(diffs, p -> if p != 0 then error ("FAIL: " | label));
    print ("PASS: " | label);
    );

exactDivX = (p,n,label) -> (
    q := (matrix{{p}} // matrix{{x^n}})_(0,0);
    if ring q =!= P then error ("wrong quotient ring: " | label);
    certCheck("exact division: " | label, p-x^n*q);
    q
    );
spaceDegree = p -> max apply(exponents p, e -> e#0+e#1+e#2);
certDegrees = (label, polys, expected) -> (
    actual := apply(polys, spaceDegree);
    if actual != expected then error ("FAIL degrees: " | label | " " | toString actual);
    print ("PASS: " | label | " degrees " | toString actual);
    );

certCheck("coefficient field relation", a^2-a+1);
certCheck("a(1-a)=1", a*(1-a)-1);
certCheck("simultaneous substitution sanity", at(y+2*z,x,z,y,t)-(z+2*y));
badDivisionRejected = try (exactDivX(1+x,1,"negative control"); false) else true;
if not badDivisionRejected then error "FAIL: non-polynomial division was accepted";
print "PASS: negative control rejects (1+x)/x";

H = (a*x^3*y^2+2*x^2*y*z+(1-a)*x*z^2
    +((a-1)*x^3-a*x)*y+(-1+a*x^2-a*x^4)*z
    -2*x^5+(6-2*a)*x^3-2*(1-a)*x);
f = (-y+x*((1-a)*y^2+2*a-2)+x^2*(2*a*y^3-5*a*y)
    +x^3*(-5*y^4+15*y^2-2*a)
    +x^4*(14*(1-a)*y^5+50*(a-1)*y^3+(29-24*a)*y));
W = exactDivX(a*(a*x*y+z-at(f,x,H,z,t)),5,"W");

chiPoly = exactDivX(a*(y-at(H,x,0_P,f,t)),5,"chi");
R = (-chiPoly+(-1+a*x^2-a*x^4+2*(1-a)*x*f)*z
    +(1-a)^2*x^6*z^2);
S = f+(1-a)*x^5*z-a*x*R;

certCheck("base H(x,R,S)=y", at(H,x,R,S,t)-y);
certCheck("base W(x,R,S)=z certificate", a*x*R+S-f-(1-a)*x^5*z);
certCheck("base R(x,H,W)=y", at(R,x,H,W,t)-y);
certCheck("base S(x,H,W)=z", at(S,x,H,W,t)-z);
certCheck("base Jacobian=-1", diff(y,H)*diff(z,W)-diff(z,H)*diff(y,W)+1);

hT = at(H,x,y+2,z-5*x,t);
wT = at(W,x,y+2,z-5*x,t);
phiT = {hT,x-hT^3+3*hT,wT-8+14*hT^2};
gammaT = {t^3-3*t,t^4-4*t^2,t^5-10*t};
certList("trefoil Phi(gamma(t))=(t,0,0)",
    apply(3, i -> at(phiT#i,gammaT#0,gammaT#1,gammaT#2,t)
        -({t,0_P,0_P}#i)));

psiT = (xx,yy,zz) -> (
    b := xx^3-3*xx+yy;
    c := zz+8-14*xx^2;
    {b, at(R,b,xx,c,t)-2, at(S,b,xx,c,t)+5*b}
    );
certList("trefoil Psi(t,0,0)=gamma(t)", psiT(t,0_P,0_P)-gammaT);
certList("trefoil normalization and outer inverse identities", {
    (y+2)-2-y, (z-5*x)+5*x-z,
    y^3-3*y+(x-y^3+3*y)-x,
    (z-8+14*y^2)+8-14*y^2-z,
    (x^3-3*x+y)-x^3+3*x-y,
    (z+8-14*x^2)-8+14*x^2-z});
certDegrees("trefoil",phiT,{5,15,24});

corr = 42*(a-1)*y^6+175*(1-a)*y^4+(147*a-161)*y^2+8;
hH = at(H,x,x*z-y^2+2,y,t);
wB = at(W,x,x*z-y^2+2,y,t);
qH = exactDivX(wB-at(corr,x,hH,z,t),1,"harmonic forward");

liftY = at(R,x,y,x*z+corr,t);
inverseY = at(S,x,y,x*z+corr,t);
inverseZ = exactDivX(liftY+inverseY^2-2,1,"harmonic inverse");

certCheck("harmonic transfer certificate", x*qH-wB+at(corr,x,hH,z,t));
certCheck("harmonic inverse certificate", x*inverseZ-inverseY^2+2-liftY);
certCheck("harmonic relative Jacobian=+1", diff(y,hH)*diff(z,qH)-diff(z,hH)*diff(y,qH)-1);

phiH = {hH,x-hH^3+3*hH,qH-(1-a)*(42*hH^3-49*hH)};
gammaH = {t^3-3*t,t^5-5*t^3+5*t,t^7-7*t^5+14*t^3-7*t};
certList("harmonic Phi(gamma(t))=(t,0,0)",
    apply(3, i -> at(phiH#i,gammaH#0,gammaH#1,gammaH#2,t)
        -({t,0_P,0_P}#i)));
psiH = (xx,yy,zz) -> (
    b := xx^3-3*xx+yy;
    c := zz+(1-a)*(42*xx^3-49*xx);
    {b,at(inverseY,b,xx,c,t),at(inverseZ,b,xx,c,t)}
    );
certList("harmonic Psi(t,0,0)=gamma(t)",psiH(t,0_P,0_P)-gammaH);
certList("harmonic outer inverse identities", {
    y^3-3*y+(x-y^3+3*y)-x,
    (z-(1-a)*(42*y^3-49*y))+(1-a)*(42*y^3-49*y)-z,
    (x^3-3*x+y)-x^3+3*x-y,
    (z+(1-a)*(42*x^3-49*x))-(1-a)*(42*x^3-49*x)-z});
certDegrees("harmonic",phiH,{7,21,41});
badGamma = {t^3-3*t,t^5-5*t^3+4*t,t^7-7*t^5+14*t^3-7*t};
if at(hH,badGamma#0,badGamma#1,badGamma#2,t) == t then
    error "FAIL: the +4t negative control unexpectedly passed";
print "PASS: negative control distinguishes +4t from +5t";

certList("harmonic x=0 forward after inverse", {
    at(hH,0_P,at(inverseY,0_P,y,z,t),at(inverseZ,0_P,y,z,t),t)-y,
    at(qH,0_P,at(inverseY,0_P,y,z,t),at(inverseZ,0_P,y,z,t),t)-z});
certList("harmonic x=0 inverse after forward", {
    at(inverseY,0_P,at(hH,0_P,y,z,t),at(qH,0_P,y,z,t),t)-y,
    at(inverseZ,0_P,at(hH,0_P,y,z,t),at(qH,0_P,y,z,t),t)-z});

print "BOTH RECTIFICATIONS VERIFIED (Macaulay2 certificates)";
