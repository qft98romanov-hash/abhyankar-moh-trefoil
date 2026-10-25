-- Expected to exit nonzero: reject a quotient with a nonzero remainder.
-- This calls the very same function used by the main certificate.
load "verify_rectification.m2";
exactDivX(1+x,1,"EXTERNAL NEGATIVE CONTROL: (1+x)/x");
error "NEGATIVE CONTROL BUG: non-polynomial quotient was accepted";
