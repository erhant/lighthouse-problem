# A Lighthouse Illumination Problem

This repository includes some codes regarding my paper ["A Lighthouse Illumination Problem"](https://arxiv.org/abs/1903.09001).

TODO: arc has problems.

There are two variations regarding how the illumination occurs, described briefly by the following figure from the paper:
<p align="center">
  <img src="/img/lighthouses.png" width="540">
</p>

## 1 - Point Light-source at the Centers

The code in `variation_1.py` is to study the first variation of the problem, where the lightsource is the center point for each lighthouse. The code first generates the lighthouses for visualization, and then it tries to find the defining ray for the target lighthouse, which is the rightmost lighthouse. Due to the symmetry of the problem, we only care about the half of the problem, in this case the upper half. We start from the target lighthouse and go counter-clockwise for the remaining lighthouses, to draw a tangent to the target. If the drawn tangent is making a line outside the illumination angle of the source lighthouse, we ignore it. The result is that, the furthest neighbor is the only one that can draw such a line. That line defines the smallest dark area behind the target lighthouse. We compare the calculation within the script and via the formula in Definition 6.1. in the paper.

![n9_1](https://github.com/erhant/lighthouse-problem/blob/main/img/9_v1.png?raw=true)

We can plot how the dark area changes with respect to number of lighthouses. For up to 500 lighthouses we get the following result:

![n500_1_plot](https://github.com/erhant/lighthouse-problem/blob/main/img/500_v1.png?raw=true)

## 2 - Point Light-sources at the Arcs

The code in `variation_2.py` is to study the second variation of the problem. I've found it quite hard to come up with a theoretical result in this, and would appreciate any help. Please also refer to the paper for more information and attempts.

![n9_2](https://github.com/erhant/lighthouse-problem/blob/main/img/9_v2.png?raw=true)

What is interesting about this case is that, occasionally the lighthouse that defines the dark area will get further away from the target. The first of such occasion occurs at precisely 20 lighthouses, also discussed in the paper.

![n20_2](https://github.com/erhant/lighthouse-problem/blob/main/img/20_v2.png?raw=true)

This _adjustment_ happens around every 10 or 9 steps from what I have seen so far empirically. In other words, starting from 20 lighthouses, each addition of around 10 lighthouses cause the source lighthouse to go further away from the target. A very intriguing plot of this is given below:

![n500_2_plot](https://github.com/erhant/lighthouse-problem/blob/main/img/500_v2.png?raw=true)

_The question:_ why is this plot like this? Why does that adjustment happen at that many steps?

## Usage

You only need Python with `numpy` and `matplotlib`.

In both variations, there are two functions: `draw_all` and `draw_match`. The input is the number of lighthouses. It will plot the lighthouses, it will show the illumination lines and the intersection of x-axis with the dark area defining ray between lighthouse 0. If you only want to see the computation, without losing time with plots, use `compute_darkness` instead. You can also obtain the plots above via `plot_results` function.
