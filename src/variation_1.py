from math import inf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D 
rcParams.update({'figure.autolayout': True})
from util import rotate, dist_2d, angle_2d, find_lighthouse_centers, find_lighthouse_illum_points
 
def find_tangent(LC_s, LC_t):
  """
  Given a source and target lighthouse center with radius 1, find the tangent. 
  
  This is done by first finding the angle between LC_t, LC_s, tang and then calculating the tang itself via rotation.
  """
  return rotate(LC_s, LC_t, np.arcsin(1/dist_2d(LC_s, LC_t)))

def get_illumination_line(LC_s, LC_t, PC, N):
  """
  Draws the illumination line from a source lighthouse to target lighthouse (variation 1: source point of light)

  Returns a boolean that shows whether it is a valid line, the tangent point, and a Line2D object to draw.
  """
  tang = find_tangent(LC_s, LC_t)
  angle = angle_2d(PC, LC_s, tang)
  alphaHalf = 180 / N
  if angle > alphaHalf:
    return False, tang, Line2D([LC_s[0], tang[0]], [LC_s[1], tang[1]], color='red', linestyle="--", linewidth=0.5)
  else:
    return True, tang, Line2D([LC_s[0], tang[0]], [LC_s[1], tang[1]], color='green', linewidth=0.5)

def get_first_illumination_line(lighthouses, PC):
  """
  Starting from the immediate upper neighbor of the target lighthouse (currently default to 0), and search counter-clockwise until you find a valid line. 
  
  The theory is that for variation 1, it shall be the furthest lighthouse that can draw a valid line.
  
  Returns the tangent, and the Line2D object.
  """
  target = lighthouses[0]
  for source in lighthouses[1:int(len(lighthouses)/2)+1]:
    isValid, tang, line = get_illumination_line(source['center'], target['center'], PC, len(lighthouses))
    if isValid:
      return source['center'], tang, line
  raise Exception("No valid illuminations!") # we dont expect this to happen

def theorem_4_3_formula(N):
  """
  Dark area calculation from the paper. 
  
  Calculation is proven by Theorem 4.3, and the definition is given in Definition 6.1.
  """
  if N == 1:
    return 0
  if N % 2 == 0:
    return inf
  PI = np.pi
  x = (np.sqrt(4*N*N*(np.cos(PI/(2*N)**2)) - 1) + 2*N*N*np.sin(PI/N)*(np.cos(PI/(2*N))**2))/(N*N*(np.sin(PI/N)**2)-1)
  return N * (x - np.arctan(x))

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

  plt.xlim([-num_lighthouses-1.5,num_lighthouses+1.5])
  plt.ylim([-num_lighthouses-1.5, num_lighthouses+1.5])
  if num_lighthouses == 1:
    DA = 0
  else:
    source, tangent, illumline = get_first_illumination_line(lighthouses, placement_center)
    ax.add_line(illumline)
    ax.scatter(source[0], source[1], color="green")
    ax.scatter(tangent[0], tangent[1], color="green")
    if source[1] <= tangent[1]:
      # The dark area is infinite
      DA = inf      
    else:
      # We can find the dark area
      coeff = np.polyfit([tangent[0], source[0]], [tangent[1], source[1]], 1) # finds the coefficients of y = ax + b for points x, y.
      target_cross_x = -coeff[1]/coeff[0] # we look for 0 = ax' + b --> x = -b/a
      ax.scatter(target_cross_x, 0.0, color="orange")
      ax.add_line(Line2D([tangent[0], target_cross_x], [tangent[1], 0.0], color='gray', linewidth=0.5))
      ax.add_line(Line2D([lighthouses[0]['center'][0], target_cross_x], [lighthouses[0]['center'][1], 0.0], color='gray', linewidth=0.5))
      x = dist_2d((target_cross_x, 0.0), tangent) # this is the nugget, we can find the dark area from this.
      DA = num_lighthouses * (x - np.arctan(x)) # Theorem 4.3
      plt.xlim([-num_lighthouses-1.5, target_cross_x+1.5])

  print("Dark Area by Calculation:",DA)
  print("Dark Area by Theorem:",theorem_4_3_formula(num_lighthouses))

  
  plt.show()