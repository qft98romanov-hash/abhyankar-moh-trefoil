# This file MUST fail with a nonzero exit status and a FAILED message.
# Run from this directory: gap -q --quitonbreak --norepl negative_identity.g
Read("verify_rectification.g");;
RectificationResult.checkZero("deliberately false identity 1=0",[One(RectificationResult.ring)]);
Error("UNREACHABLE: checker accepted 1=0");
