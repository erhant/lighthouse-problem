import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams 
rcParams.update({'figure.autolayout': True})

def rotate(origin, point, angle_rad):
  """
  Rotate a point counterclockwise by a given angle around a given origin.

  The angle should be given in radians.

  Source: https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
  """
  ox, oy = origin
  px, py = point

  qx = ox + np.cos(angle_rad) * (px - ox) - np.sin(angle_rad) * (py - oy)
  qy = oy + np.sin(angle_rad) * (px - ox) + np.cos(angle_rad) * (py - oy)
  return (qx, qy)

def find_lighthouse_centers(N, PC):
  alpha_rad = np.radians(360.0 / N)
  centers = []
  centers.append((PC[0] + N, PC[1]))
  for i in range(1, N):
    centers.append(rotate(PC, centers[0], alpha_rad * i))
  return centers


if __name__ == "__main__":
  num_lighthouses = 3
  assert(num_lighthouses > 0)
  placement_center = (0.0, 0.0)
  centers = find_lighthouse_centers(num_lighthouses, placement_center)
  print(centers)

  # plots
  fig = plt.figure()
  ax = plt.axes()
  ax.scatter(placement_center[0], placement_center[1], color="red")
  for c in centers:
    ax.add_patch(plt.Circle(c, 1.0, color='black', fill=False))
  plt.xlim([-num_lighthouses-1.5, num_lighthouses+1.5])
  plt.ylim([-num_lighthouses-1.5, num_lighthouses+1.5])
  plt.show()