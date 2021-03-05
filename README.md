# A Lighthouse Illumination Problem
This repository includes some codes to investigate my paper ["A Lighthouse Illumination Problem"](https://arxiv.org/abs/1903.09001).

## Variation 1
The code in `variation_1.py` is to study the first variation of the problem, where the lightsource is the center point for each lighthouse. The code first generates the lighthouses for visualization, and then it tries to find the defining ray for the target lighthouse, which is the rightmost lighthouse. Due to the symmetry of the problem, we only care about the half of the problem, in this case the upper half. We start from the target lighthouse and go counter-clockwise for the remaining lighthouses, to draw a tangent to the target. If the drawn tangent is making a line outside the illumination angle of the source lighthouse, we ignore it. 

The result is that, the furthest neighbor is the only one that can draw such a line. That line defines the smallest dark area behind the target lighthouse.

We compare the calculation within the script and via the formula in Definition 6.1. in the paper. 

## Variation 2
The code in `variation_2.py` is to study the second variation of the problem, _work in progress..._