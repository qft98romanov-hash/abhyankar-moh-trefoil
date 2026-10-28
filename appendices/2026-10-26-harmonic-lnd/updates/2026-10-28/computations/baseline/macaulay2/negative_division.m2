-- Consolidated verification copy, 28 October 2026.
-- Exact source statements are unchanged; original logs are historical evidence.
-- This interpreter is optional and is not required by the Python certificate suite.
-- Expected to exit nonzero: reject a quotient with a nonzero remainder.
-- This calls the very same function used by the main certificate.
load "./verify_rectification.m2";
exactDivX(1+x,1,"EXTERNAL NEGATIVE CONTROL: (1+x)/x");
error "NEGATIVE CONTROL BUG: non-polynomial quotient was accepted";
