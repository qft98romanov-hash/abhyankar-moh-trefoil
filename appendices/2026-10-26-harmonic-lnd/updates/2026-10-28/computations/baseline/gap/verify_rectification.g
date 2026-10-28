# Consolidated verification copy, 28 October 2026.
# Exact source statements are unchanged; original logs are historical evidence.
# This interpreter is optional and is not required by the Python certificate suite.
# -*- coding: utf-8 -*-
# Exact GAP verification of two rectifications, without Python or extra packages.
# In GAP: Read("C:/rectification_check/gap/verify_rectification.g");
# Coefficients lie in Q(E(3)); a=E(6)=(1+sqrt(-3))/2.
# No floating-point arithmetic or random point evaluations are used.

RunRectificationVerification := function(a)
    local K, P, vars, x, y, z, t, one, zero, start, count,
          Check, At, ExactDivX, TotalDegree, CheckDegrees,
          H, f, W, chi, R, S, ht, wt, phiT, invT,
          correction, hh, wb, qh, ly, iy, iz, phiH, invH,
          cT, cH, outerT, outerTi, outerH, outerHi, wrongCurve, i;

    start := Runtime();
    count := 0;
    K := CyclotomicField(3);
    P := PolynomialRing(K, ["x", "y", "z", "t"]);
    vars := IndeterminatesOfPolynomialRing(P);
    x := vars[1]; y := vars[2]; z := vars[3]; t := vars[4];
    one := One(P); zero := Zero(P);

    # A failed check stops execution before the final success marker.
    Check := function(label, differences)
        local p;
        for p in differences do
            if not IsZero(p) then
                Error(Concatenation("FAILED: ", label));
            fi;
        od;
        count := count + 1;
        Print("PASS ", count, ": ", label, "\n");
    end;

    # SIMULTANEOUS substitution in four independent polynomial variables.
    At := function(p, xx, yy, zz, tt)
        return Value(p, vars, [xx, yy, zz, tt], one);
    end;

    # Division takes place in the polynomial ring, not its fraction field.
    # All coefficients of x^0,...,x^(n-1) must vanish.
    ExactDivX := function(p, n, label)
        local coeff, i, q;
        if IsZero(p) then
            return zero;
        fi;
        coeff := PolynomialCoefficientsOfPolynomial(p, x);
        for i in [1..Minimum(n, Length(coeff))] do
            if not IsZero(coeff[i]) then
                Error(Concatenation("NOT DIVISIBLE: ", label));
            fi;
        od;
        q := zero;
        if Length(coeff) > n then
            for i in [n+1..Length(coeff)] do
                q := q + coeff[i] * x^(i-1-n);
            od;
        fi;
        Check(Concatenation("exact division ", label), [p-x^n*q]);
        return q;
    end;

    # Total degree in x,y,z,t; the map components below do not involve t.
    # External representation: [monomial, coefficient, monomial, coefficient,...].
    TotalDegree := function(p)
        local rep, i, j, mon, d, answer;
        if IsZero(p) then return -1; fi;
        rep := ExtRepPolynomialRatFun(p);
        answer := 0;
        i := 1;
        while i <= Length(rep) do
            mon := rep[i]; d := 0; j := 2;
            while j <= Length(mon) do
                d := d + mon[j]; j := j + 2;
            od;
            answer := Maximum(answer, d); i := i + 2;
        od;
        return answer;
    end;

    CheckDegrees := function(label, polys, expected)
        local actual;
        actual := List(polys, TotalDegree);
        if actual <> expected then
            Error(Concatenation("WRONG DEGREES: ", label));
        fi;
        count := count + 1;
        Print("PASS ", count, ": ", label, " ", actual, "\n");
    end;

    Print("GAP ", GAPInfo.Version, " exact rectification verification\n");
    Print("Coefficient a = ", a, "; arithmetic in Q(E(3)).\n");
    Check("coefficient field", [a^2-a+1, a*(1-a)-1]);
    Check("simultaneous substitution",
          [At(x+2*y+3*z+t,y,z,x,t)-(y+2*z+3*x+t)]);

    # Base automorphism A=(x,H,W). Formulas are entered directly.
    H := a*x^3*y^2+2*x^2*y*z+(1-a)*x*z^2
         +((a-1)*x^3-a*x)*y+(-1+a*x^2-a*x^4)*z
         -2*x^5+(6-2*a)*x^3-2*(1-a)*x;
    f := -y+x*((1-a)*y^2+2*a-2)+x^2*(2*a*y^3-5*a*y)
         +x^3*(-5*y^4+15*y^2-2*a)
         +x^4*(14*(1-a)*y^5+50*(a-1)*y^3+(29-24*a)*y);
    W := ExactDivX(a*(a*x*y+z-At(f,x,H,z,t)),5,"W");
    chi := ExactDivX(a*(y-At(H,x,zero,f,t)),5,"chi");
    R := -chi+(-1+a*x^2-a*x^4+2*(1-a)*x*f)*z
         +(1-a)^2*x^6*z^2;
    S := f+(1-a)*x^5*z-a*x*R;

    Check("base H(x,R,S)=y", [At(H,x,R,S,t)-y]);
    Check("base certificate for W(x,R,S)=z",
          [a*x*R+S-f-(1-a)*x^5*z]);
    # The preceding identities and the definition of W imply
    # x^5*(W(x,R,S)-z)=0. Cancel x^5 in the domain K[x,y,z].
    Check("base R(x,H,W)=y", [At(R,x,H,W,t)-y]);
    Check("base S(x,H,W)=z", [At(S,x,H,W,t)-z]);
    Check("base relative Jacobian = -1",
          [Derivative(H,y)*Derivative(W,z)-Derivative(H,z)*Derivative(W,y)+1]);

    # TREFOIL: first apply (x,y,z) -> (x,y+2,z-5x).
    ht := At(H,x,y+2,z-5*x,t);
    wt := At(W,x,y+2,z-5*x,t);
    phiT := [ht, x-ht^3+3*ht, wt-8+14*ht^2];
    invT := [x^3-3*x+y,
             At(R,x^3-3*x+y,x,z+8-14*x^2,t)-2,
             At(S,x^3-3*x+y,x,z+8-14*x^2,t)+5*(x^3-3*x+y)];
    Check("trefoil affine normalization and inverse",
          [(y+2)-2-y, (z-5*x)+5*x-z]);
    outerT := [y,x-y^3+3*y,z-8+14*y^2];
    outerTi := [x^3-3*x+y,x,z+8-14*x^2];
    Check("trefoil outer maps: both compositions",
          Concatenation(
            List([1..3],i->At(outerT[i],outerTi[1],outerTi[2],outerTi[3],t)-vars[i]),
            List([1..3],i->At(outerTi[i],outerT[1],outerT[2],outerT[3],t)-vars[i])));
    cT := [t^3-3*t,t^4-4*t^2,t^5-10*t];
    Check("trefoil Phi(gamma(t))=(t,0,0)",
          List([1..3],i->At(phiT[i],cT[1],cT[2],cT[3],t)-[t,zero,zero][i]));
    Check("trefoil inverse on axis",
          List([1..3],i->At(invT[i],t,zero,zero,t)-cT[i]));
    CheckDegrees("trefoil forward degrees",phiT,[5,15,24]);

    # HARMONIC FIGURE-EIGHT: the second component has linear term +5t.
    correction := 42*(a-1)*y^6+175*(1-a)*y^4+(147*a-161)*y^2+8;
    hh := At(H,x,x*z-y^2+2,y,t);
    wb := At(W,x,x*z-y^2+2,y,t);
    qh := ExactDivX(wb-At(correction,x,hh,z,t),1,"harmonic forward");
    ly := At(R,x,y,x*z+correction,t);
    iy := At(S,x,y,x*z+correction,t);
    iz := ExactDivX(ly+iy^2-2,1,"harmonic inverse");

    # Additional exact checks of the centre on the exceptional fibre x=0.
    Check("harmonic centre at x=0 is -y", [At(hh,zero,y,z,t)+y]);
    Check("harmonic companion on centre",
          [At(wb,zero,y,z,t)-At(correction,zero,-y,z,t)]);
    Check("harmonic relative Jacobian = +1",
          [Derivative(hh,y)*Derivative(qh,z)-Derivative(hh,z)*Derivative(qh,y)-1]);

    # Over K[x,1/x,y,z], the relative map (x,hh,qh) is
    # (x,y,(z-correction(y))/x) o (x,H,W) o (x,xz-y^2+2,y).
    # Its inverse is obtained by inverting the factors in reverse order.
    # ExactDivX has established polynomiality of both resulting maps.
    # Injectivity of K[x,y,z] -> K[x,1/x,y,z] extends BOTH composition
    # identities to all of affine space, including x=0.
    phiH := [hh,x-hh^3+3*hh,qh-(1-a)*(42*hh^3-49*hh)];
    invH := [x^3-3*x+y,
             At(iy,x^3-3*x+y,x,z+(1-a)*(42*x^3-49*x),t),
             At(iz,x^3-3*x+y,x,z+(1-a)*(42*x^3-49*x),t)];
    outerH := [y,x-y^3+3*y,z-(1-a)*(42*y^3-49*y)];
    outerHi := [x^3-3*x+y,x,z+(1-a)*(42*x^3-49*x)];
    Check("harmonic outer maps: both compositions",
          Concatenation(
            List([1..3],i->At(outerH[i],outerHi[1],outerHi[2],outerHi[3],t)-vars[i]),
            List([1..3],i->At(outerHi[i],outerH[1],outerH[2],outerH[3],t)-vars[i])));
    cH := [t^3-3*t,t^5-5*t^3+5*t,t^7-7*t^5+14*t^3-7*t];
    Check("harmonic Phi(gamma(t))=(t,0,0)",
          List([1..3],i->At(phiH[i],cH[1],cH[2],cH[3],t)-[t,zero,zero][i]));
    Check("harmonic inverse on axis",
          List([1..3],i->At(invH[i],t,zero,zero,t)-cH[i]));
    CheckDegrees("harmonic forward degrees",phiH,[7,21,41]);

    # Negative control: +4t specifies a DIFFERENT curve. These formulas
    # must not report that this different curve is rectified to the axis.
    wrongCurve := [t^3-3*t,t^5-5*t^3+4*t,t^7-7*t^5+14*t^3-7*t];
    if IsZero(At(phiH[1],wrongCurve[1],wrongCurve[2],wrongCurve[3],t)-t) then
        Error("FAILED: negative control did not detect +4t instead of +5t");
    fi;
    count := count+1;
    Print("PASS ",count,": negative control rejects the +4t model\n");

    Print("BOTH RECTIFICATIONS VERIFIED IN GAP\n");
    Print("Checks: ",count,"; runtime (CPU ms): ",Runtime()-start,"\n");
    # Return all maps for optional direct inspection.
    return rec(field:=K,a:=a,ring:=P,variables:=vars,base:=[x,H,W],
               baseInverse:=[x,R,S],trefoil:=phiT,trefoilInverse:=invT,
               harmonic:=phiH,harmonicInverse:=invH,checks:=count,
               checkZero:=Check,exactDivX:=ExactDivX);
end;

RectificationResult := RunRectificationVerification(E(6));;
# Repeat for the complex-conjugate coefficient.
ConjugateResult := RunRectificationVerification(1-E(6));;

# Extra checks: the Chebyshev notation is an affine normalization of
# the already verified trefoil, not a third independent construction.
# C_n(t)=2*T_n(t/2), so C_0=2, C_1=t, C_(n+1)=t*C_n-C_(n-1).
RunChebyshevVerification := function(result)
    local vars, x, y, z, t, one, zero, C, n, At, CheckExtra,
          count, cT, cC, cH, M, Mi, differences, i,
          chebyshevForward, chebyshevInverse;
    vars := result.variables;
    x := vars[1]; y := vars[2]; z := vars[3]; t := vars[4];
    one := One(result.ring); zero := Zero(result.ring);
    count := 0;
    At := function(p, images)
        return Value(p, vars, Concatenation(images,[t]), one);
    end;
    CheckExtra := function(label, differences)
        if ForAny(differences, p -> not IsZero(p)) then
            Error(Concatenation("FAILED Chebyshev check: ",label));
        fi;
        count := count+1;
        Print("EXTRA PASS ",count,": ",label,"\n");
    end;
    C := [2*one,t];
    for n in [1..6] do Add(C,t*C[n+1]-C[n]); od;
    cT := [t^3-3*t,t^4-4*t^2,t^5-10*t];
    cC := [C[4],C[5],C[6]];
    cH := [C[4],C[6],C[8]];
    M := [x,y+2,z-5*x];
    Mi := [x,y-2,z+5*x];
    differences := Concatenation(
        List([1..3],i->At(M[i],Mi)-vars[i]),
        List([1..3],i->At(Mi[i],M)-vars[i]),
        List([1..3],i->At(M[i],cT)-cC[i]));
    CheckExtra("M and its inverse; M(gamma_T)=(C3,C4,C5)",differences);
    CheckExtra("harmonic gamma_H=(C3,C5,C7)",
        [cH[1]-(t^3-3*t),cH[2]-(t^5-5*t^3+5*t),
         cH[3]-(t^7-7*t^5+14*t^3-7*t)]);
    # Phi_C=Phi_T o M^-1; its global inverse is M o Phi_T^-1.
    # Their global inverse identities follow by composing the already
    # certified inverse pair with the verified affine inverse pair M,Mi.
    chebyshevForward := List(result.trefoil,p->At(p,Mi));
    chebyshevInverse := List(M,p->At(p,result.trefoilInverse));
    CheckExtra("transported Chebyshev rectifier and inverse on the axis",
        Concatenation(
            List([1..3],i->At(chebyshevForward[i],cC)-[t,zero,zero][i]),
            List([1..3],i->At(chebyshevInverse[i],[t,zero,zero])-cC[i])));
    Print("CHEBYSHEV NORMALIZATIONS VERIFIED; additional checks: ",count,"\n");
    return rec(curve:=cC,forward:=chebyshevForward,
               inverse:=chebyshevInverse,checks:=count);
end;

ChebyshevResult := RunChebyshevVerification(RectificationResult);;
ConjugateChebyshevResult := RunChebyshevVerification(ConjugateResult);;
