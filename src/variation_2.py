from math import inf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D 
rcParams.update({'figure.autolayout': True})
from util import rotate, dist_2d, angle_2d, find_lighthouse_centers, find_lighthouse_illum_points


def checkCollision(a, b, c, x, y, r):
  """
  Find if there is a collision of a line & circle. The line is in form ax+by+c=0 and circle is at center (x,y) with radius r.
  If the line does not collide or is tangent, we say there is no collision.

  Source: https://www.geeksforgeeks.org/check-line-touches-intersects-circle/
  """ 
      
  # Finding the distance of line  
  # from center. 
  d = ((abs(a * x + b * y + c)) / np.sqrt(a * a + b * b)) 

  # Checking if the distance is less  
  # than, greater than or equal to radius. 
  if (r == d): # line is tangent
    return False
  elif (r > d): # line is inside
    return True
  elif (r < d): # line is outside
    return False
        
def find_tangent(LL_s, LC_t):
  """
  Given a source point and target lighthouse center with radius 1, find the tangent. 
  
  This is done by first finding the angle between LC_t, LL_s, tang and then calculating the tang itself via rotation. LL is "Lighthouse->Left". 
  It is possible that the angle between the supposed 
  """
  return rotate(LL_s, LC_t, np.arcsin(1/dist_2d(LL_s, LC_t)))

def get_illumination_line(LL_s, LC_t):
  """
  Draws the illumination line from a source lighthouse to target lighthouse (variation 1: source point of light)

  Returns a boolean that shows whether it is a valid line, the tangent point, and a Line2D object to draw.
  """
  tang = find_tangent(LL_s, LC_t) 
  return tang, Line2D([LL_s[0], tang[0]], [LL_s[1], tang[1]], color='orange', linewidth=0.5)

def get_first_illumination_line(lighthouses):
  """
  Finds the first valid illumination line in second variation.

  TODO: ERRORS HERE, NEED TO FIX
  """
  target = lighthouses[0]
  
  for i in range(1,int(len(lighthouses)/2)):
    print(i)
    source = lighthouses[i]
    tang = find_tangent(source['left'], target['center']) # find tangent
    coeff = np.polyfit([source['left'][0], tang[0]], [source['left'][1], tang[1]], 1) # finds the coefficients of y = px + q for points x, y.
    for l in lighthouses[1:i+1]: # check if it collides with anything in between 
      print("ey")
      # y = px + q --> -px + y -q = 0
      if not checkCollision(-coeff[0], 1, -coeff[1], l['center'][0], l['center'][1], 1):
        return source['left'], tang, Line2D([source['left'][0], tang[0]], [source['left'][1], tang[1]], color='green', linewidth=0.5)


if __name__ == "__main__":
  num_lighthouses = 4
  assert(num_lighthouses > 0)
  placement_center = (0.0, 0.0)
  centers = find_lighthouse_centers(num_lighthouses, placement_center)
  lighthouses = []
  for c in centers:
    left, mid, right = find_lighthouse_illum_points(num_lighthouses, c, placement_center)
    lighthouses.append({
      "center": c,
      "left": left,
      "middle": mid,
      "right": right
    })

  # plots
  fig = plt.figure()
  ax = plt.axes()
  ax.scatter(placement_center[0], placement_center[1], color="red")
  for l in lighthouses:
    ax.add_patch(plt.Circle(l['center'], 1.0, color='black', fill=False))
    ax.scatter(l['center'][0], l['center'][1], color="yellow")
    ax.scatter(l['left'][0], l['left'][1], color="gray")
    ax.scatter(l['right'][0], l['right'][1], color="gray")
    ax.scatter(l['middle'][0], l['middle'][1], color="gray")
    ax.add_line(Line2D([l['center'][0], placement_center[0]], [l['center'][1], placement_center[1]], linestyle='--', color='gray', linewidth=0.4))
    ax.add_line(Line2D([l['center'][0], l['left'][0]], [l['center'][1], l['left'][1]], color='gray', linewidth=0.5))
    ax.add_line(Line2D([l['center'][0], l['right'][0]], [l['center'][1], l['right'][1]], color='gray', linewidth=0.5))

  source, tangent, illumline = get_first_illumination_line(lighthouses)
  ax.add_line(illumline)
  ax.scatter(source[0], source[1], color="green")
  ax.scatter(tangent[0], tangent[1], color="green")

  plt.xlim([-num_lighthouses-1.5,num_lighthouses+1.5])
  plt.ylim([-num_lighthouses-1.5, num_lighthouses+1.5])
  plt.show()