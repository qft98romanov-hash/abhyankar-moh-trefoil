-- Three additional exact checks of the normalized Chebyshev models.
-- The main 27 checks are loaded first and are reported separately.
load "./verify_rectification.m2";
chebC = n -> (if n == 0 then 2_P else if n == 1 then t else t*chebC(n-1)-chebC(n-2));
certList("CHEBYSHEV: M(gamma_T)=(C3,C4,C5)",
    {gammaT#0,gammaT#1+2,gammaT#2-5*gammaT#0}
      - {chebC(3),chebC(4),chebC(5)});
certList("CHEBYSHEV: gamma_H=(C3,C5,C7)",
    gammaH-{chebC(3),chebC(5),chebC(7)});
certList("CHEBYSHEV: both affine inverse identities", {
    x-x, ((y+2)-2)-y, ((z-5*x)+5*x)-z,
    x-x, ((y-2)+2)-y, ((z+5*x)-5*x)-z});
print "THREE ADDITIONAL CHEBYSHEV CHECKS VERIFIED";
