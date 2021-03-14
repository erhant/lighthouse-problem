from math import inf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D 
rcParams.update({'figure.autolayout': True})
from util import rotate, dist_2d, angle_2d, find_lighthouse_centers, find_lighthouse_illum_points

def checkCollision(x1, y1, x2, y2, cx, cy, r):
  """
  Find if there is a collision of a line & circle. The line is between (x1, y1) and (x2, y2). Circle is at (cx, cy) with radius r.

  Source: https://math.stackexchange.com/a/275533 
  """ 
      
  # Finding the distance of line  
  # from center. 
  a = y1 - y2
  b = x2 - x1
  c = -(b*y1 + a*x1)
  dist = ((abs(a * cx + b * cy + c)) / np.sqrt(a * a + b * b)) 

  # Checking if the distance is less  
  # than, greater than or equal to radius. 
  if (r == dist): # line is tangent
    return False
  elif (r > dist): # line is inside
    return True
  elif (r < dist): # line is outside
    return False
        
def find_tangent(LL_s, LC_t):
  """
  Given a source point and target lighthouse center with radius 1, find the tangent. 
  
  This is done by first finding the angle between LC_t, LL_s, tang and then calculating the tang itself via rotation. LL is "Lighthouse->Left". 
  It is possible that the angle between the supposed 
  """
  return rotate(LL_s, LC_t, np.arcsin(1/dist_2d(LL_s, LC_t)))

def get_illumination_line(lighthouses_between, LC_s, LL_s, LC_t):
  """
  Draws the illumination line from a source lighthouse to target lighthouse (variation 2: source point of light)

  Returns a boolean that shows whether it is a valid line, the tangent point, and a Line2D object to draw.
  """
  tang = find_tangent(LL_s, LC_t) 
  
  if angle_2d(tang, LL_s, LC_s) < 90:
    # if angle LC_s, LL_s, tang angle is less than 90 its a problem at the source 
    return False, tang, Line2D([LL_s[0], tang[0]], [LL_s[1], tang[1]], color='red', linestyle="--", linewidth=0.5)
  else:
    # source is okay, see if it collides with anything in between
    for lighthouse in lighthouses_between:
      if checkCollision(LL_s[0], LL_s[1], tang[0], tang[1], lighthouse['center'][0], lighthouse['center'][1], 1.0):
        return False, tang, Line2D([LL_s[0], tang[0]], [LL_s[1], tang[1]], color='red', linestyle="--", linewidth=0.5)

    # no collisions
    return True, tang, Line2D([LL_s[0], tang[0]], [LL_s[1], tang[1]], color='green', linewidth=0.5)

def get_first_illumination_line(lighthouses):
  """
  Finds the first valid illumination line in second variation. 
  """
  target = lighthouses[0]
  cur = 1 
  for source in lighthouses[1:int(len(lighthouses)/2)+1]:
    isValid, tang, line = get_illumination_line(lighthouses[1:cur], source['center'], source['left'], target['center'])
    if isValid:
      return source['left'], tang, line
    cur += 1
  raise Exception("No valid illuminations!") # we dont expect this to happen (but maybe it is possible :o)

def draw_all(N):
  '''
  Draw all lines until a match.
  '''
  placement_center = (0.0, 0.0)
  centers = find_lighthouse_centers(N, placement_center)
  lighthouses = []
  for c in centers:
    left, mid, right = find_lighthouse_illum_points(N, c, placement_center)
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
 
  target = lighthouses[0]
  cur = 1 
  for source in lighthouses[1:int(len(lighthouses)/2)+1]:
    isValid, tang, line = get_illumination_line(lighthouses[1:cur], source['center'], source['left'], target['center'])
    ax.add_line(line) 
    if isValid:
      ax.scatter(source['left'][0], source['left'][1], color="green")
      ax.scatter(tang[0], tang[1], color="green") 
      break
    else:
      ax.scatter(source['left'][0], source['left'][1], color="red")
      ax.scatter(tang[0], tang[1], color="red") 
    cur += 1 

  plt.xlim([-N-1.5, N+1.5])
  if N == 1:
    DA = 0
  elif N == 2:
    DA = inf
  else:
    # We can find the dark area
    coeff = np.polyfit([tang[0], source['left'][0]], [tang[1], source['left'][1]], 1) # finds the coefficients of y = ax + b for points x, y.
    target_cross_x = -coeff[1]/coeff[0] # we look for 0 = ax' + b --> x = -b/a
    ax.scatter(target_cross_x, 0.0, color="orange")
    ax.add_line(Line2D([tang[0], target_cross_x], [tang[1], 0.0], color='gray', linewidth=0.5))
    ax.add_line(Line2D([lighthouses[0]['center'][0], target_cross_x], [lighthouses[0]['center'][1], 0.0], color='gray', linewidth=0.5))
    x = dist_2d((target_cross_x, 0.0), tang) # this is the nugget, we can find the dark area from this.
    DA = N * (x - np.arctan(x)) # Theorem 4.3
    plt.xlim([-N-1.5, target_cross_x+1.5])
  plt.ylim([-N-1.5, N+1.5])

  print("D("+str(N)+") by Calculation:",DA)

  ax.set_title(str(N)+" lighthouses")
  plt.show()
  return DA

def draw_match(N):
  '''
  Draw the matching line only
  '''
  placement_center = (0.0, 0.0)
  centers = find_lighthouse_centers(N, placement_center)
  lighthouses = []
  for c in centers:
    left, mid, right = find_lighthouse_illum_points(N, c, placement_center)
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

  source, tang, illumline = get_first_illumination_line(lighthouses)
  ax.add_line(illumline)
  ax.scatter(source[0], source[1], color="green")
  ax.scatter(tang[0], tang[1], color="green")

  plt.xlim([-N-1.5, N+1.5])
  
  if N == 1:
    DA = 0
  elif N == 2:
    DA = inf
  else:
    # We can find the dark area
    coeff = np.polyfit([tang[0], source[0]], [tang[1], source[1]], 1) # finds the coefficients of y = ax + b for points x, y.
    target_cross_x = -coeff[1]/coeff[0] # we look for 0 = ax' + b --> x = -b/a
    ax.scatter(target_cross_x, 0.0, color="orange")
    ax.add_line(Line2D([tang[0], target_cross_x], [tang[1], 0.0], color='gray', linewidth=0.5))
    ax.add_line(Line2D([lighthouses[0]['center'][0], target_cross_x], [lighthouses[0]['center'][1], 0.0], color='gray', linewidth=0.5))
    x = dist_2d((target_cross_x, 0.0), tang) # this is the nugget, we can find the dark area from this.
    DA = N * (x - np.arctan(x)) # Theorem 4.3
    plt.xlim([-N-1.5, target_cross_x+1.5]) 

  print("D("+str(N)+") by Calculation:",DA)

  plt.ylim([-N-1.5, N+1.5])

  ax.set_title(str(N)+" lighthouses")
  plt.show()
  return DA

def compute_darkness(N, print_res=True):
  if N == 1:
    DA = 0
  elif N == 2:
    DA = inf
  else:
    placement_center = (0.0, 0.0)
    centers = find_lighthouse_centers(N, placement_center)
    lighthouses = []
    for c in centers:
      left, mid, right = find_lighthouse_illum_points(N, c, placement_center)
      lighthouses.append({
        "center": c,
        "left": left,
        "middle": mid,
        "right": right
      })

    source, tang, _ = get_first_illumination_line(lighthouses)

    # We can find the dark area
    coeff = np.polyfit([tang[0], source[0]], [tang[1], source[1]], 1) # finds the coefficients of y = ax + b for points x, y.
    target_cross_x = -coeff[1]/coeff[0] # we look for 0 = ax' + b --> x = -b/a 
    x = dist_2d((target_cross_x, 0.0), tang) # this is the nugget, we can find the dark area from this.
    DA = N * (x - np.arctan(x)) # Theorem 4.3
  if print_res:
    print("D("+str(N)+") by Calculation:",DA)    
  return DA

def plot_results(maxL):
  '''
  Plotting code from the notebook. Plot the results upto a given number of lighthouses.
  '''
  N_L = range(1,maxL+1)
  DA = [compute_darkness(N, print_res=False) for N in N_L]
  fig = plt.figure()
  ax = plt.axes()
  ax.scatter(N_L, DA, c='blue')

  # lets find when the area increases
  N_L_increase = [i+1 for i in range(2,len(DA)-1) if DA[i] < DA[i+1]]
  ax.scatter(N_L_increase, [0.0] * len(N_L_increase), c='orange', marker='x')
  print(N_L_increase)
  ax.set_xlabel("Number of Lighthouses")
  ax.set_ylabel("Total Dark Area")
  plt.show()

if __name__ == "__main__":
  num_lighthouses = 20
  assert(num_lighthouses > 0)
  draw_all(num_lighthouses)
  #compute_darkness(num_lighthouses)
  #plot_results(500)

  