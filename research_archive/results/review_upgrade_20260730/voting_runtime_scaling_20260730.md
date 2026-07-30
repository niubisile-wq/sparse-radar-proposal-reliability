# Strict voting runtime scaling audit (seed 2028)

One warm-up frame is excluded from the reported moments. Measures the dense 3D-IoU kernel and the Python voting loop on frozen RDAR predictions; detector inference and serialization are excluded.

| Dataset | Proposals | Dense IoU ms/frame | Voting loop ms/frame | Total ms/frame | Peak GPU MB | Neighbor links |
|---|---:|---:|---:|---:|---:|---:|
| astyx | 50 | 0.660 ± 0.024 | 0.906 ± 0.058 | 1.566 | 0.1 | 8934 |
| astyx | 100 | 0.661 ± 0.015 | 1.758 ± 0.073 | 2.420 | 0.3 | 24432 |
| astyx | 250 | 0.678 ± 0.014 | 4.497 ± 0.110 | 5.175 | 1.7 | 83918 |
| astyx | 500 | 0.645 ± 0.068 | 9.426 ± 0.494 | 10.071 | 6.7 | 206472 |
| truckscenes | 50 | 0.652 ± 0.018 | 0.888 ± 0.044 | 1.540 | 0.1 | 6648 |
| truckscenes | 100 | 0.651 ± 0.008 | 1.707 ± 0.055 | 2.358 | 0.3 | 16942 |
| truckscenes | 250 | 0.674 ± 0.010 | 4.358 ± 0.135 | 5.032 | 1.7 | 54886 |
| truckscenes | 500 | 0.628 ± 0.072 | 9.046 ± 0.592 | 9.674 | 6.7 | 131160 |
| v2xradarv | 50 | 0.637 ± 0.018 | 0.913 ± 0.053 | 1.550 | 0.1 | 7148 |
| v2xradarv | 100 | 0.636 ± 0.008 | 1.749 ± 0.062 | 2.385 | 0.3 | 18988 |
| v2xradarv | 250 | 0.653 ± 0.008 | 4.448 ± 0.096 | 5.101 | 1.7 | 63862 |
| v2xradarv | 500 | 0.616 ± 0.110 | 8.617 ± 1.709 | 9.233 | 6.7 | 158010 |
| kradar | 50 | 0.646 ± 0.023 | 0.876 ± 0.049 | 1.522 | 0.1 | 5310 |
| kradar | 100 | 0.643 ± 0.008 | 1.733 ± 0.063 | 2.376 | 0.3 | 14662 |
| kradar | 250 | 0.668 ± 0.009 | 4.492 ± 0.084 | 5.160 | 1.7 | 59842 |
| kradar | 500 | 0.609 ± 0.131 | 8.438 ± 1.854 | 9.047 | 6.7 | 148432 |
