import numpy as np


def dist_2d(p1, p2):
  """
  Distance between two points in 2D.
  """
  return np.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

def angle_2d(p1, p2, p3):
  """
  Angle between 3 points p1, p2, p3. 

      p1
    /
   / 
  p2 _ _ _ p3

  Source: https://python-forum.io/Thread-finding-angle-between-three-points-on-a-2d-graph 
  """
  ang = np.degrees(np.arctan2(p3[1]-p2[1], p3[0]-p2[0]) - np.arctan2(p1[1]-p2[1], p1[0]-p2[0]))
  return ang + 360 if ang < 0 else ang

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
  """
  Calculate the center coordinates of lighthouses.
  """
  alpha_rad = np.radians(360.0 / N)
  centers = []
  centers.append((PC[0] + N, PC[1]))
  for i in range(1, N):
    centers.append(rotate(PC, centers[i-1], alpha_rad)) # TODO: can refactor this, calculates the sin cos everytime...
  return centers

def find_lighthouse_illum_points(N, LC, PC):
  """
  Calculate the edges of the illumination angle.
  """
  mid = (((N-1)*LC[0] + PC[0])/N, ((N-1)*LC[1] + PC[1])/N)
  alpha_rad = np.radians(360.0 / N)
  return [rotate(LC, mid, alpha_rad/2), mid, rotate(LC, mid, -alpha_rad/2)] # left middle right