# This file MUST fail with a nonzero exit status and NOT DIVISIBLE.
# Run from this directory: gap -q --quitonbreak --norepl negative_division.g
Read("verify_rectification.g");;
RectificationResult.exactDivX(One(RectificationResult.ring),1,"deliberate 1/x");
Error("UNREACHABLE: checker accepted non-polynomial 1/x");
