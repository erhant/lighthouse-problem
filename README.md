# A Lighthouse Illumination Problem
This repository includes some codes regarding my paper ["A Lighthouse Illumination Problem"](https://arxiv.org/abs/1903.09001).

There are two variations regarding how the illumination occurs, described briefly by the following figure from the paper:
<p align="center">
  <img src="/img/lighthouses.png" width="540">
</p>

## 1 - Point Light-source at the Centers
The code in `variation_1.py` is to study the first variation of the problem, where the lightsource is the center point for each lighthouse. The code first generates the lighthouses for visualization, and then it tries to find the defining ray for the target lighthouse, which is the rightmost lighthouse. Due to the symmetry of the problem, we only care about the half of the problem, in this case the upper half. We start from the target lighthouse and go counter-clockwise for the remaining lighthouses, to draw a tangent to the target. If the drawn tangent is making a line outside the illumination angle of the source lighthouse, we ignore it. The result is that, the furthest neighbor is the only one that can draw such a line. That line defines the smallest dark area behind the target lighthouse. We compare the calculation within the script and via the formula in Definition 6.1. in the paper. 

![n9](https://github.com/erhant/lighthouse-problem/blob/main/img/n9_1.png?raw=true)

## 2 - Point Light-sources at the Arcs
The code in `variation_2.py` is to study the second variation of the problem, **however there are currently bugs related to precision** in the code. For example `n=4` is buggy, and the results here don't match GeoGebra results. 

![n13](https://github.com/erhant/lighthouse-problem/blob/main/img/n13_2.png?raw=true)

## To-Do List
- [ ] Add a calculation only function in variation 1, without plotting the lighthouses.
- [ ] Fix precision bug in variation 2, especially look at `n=4`.