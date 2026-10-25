-- Expected to exit nonzero: a perturbed parameter lift is not a lift.
-- This calls the actual polynomial and assertion helper from the main script.
load "verify_rectification.m2";
certCheck("EXTERNAL NEGATIVE CONTROL: perturbed trefoil lift",
    at(hT+1,gammaT#0,gammaT#1,gammaT#2,t)-t);
error "NEGATIVE CONTROL BUG: false identity was accepted";
