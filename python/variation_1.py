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

  plt.xlim([-N-1.5, N+1.5])
  plt.ylim([-N-1.5, N+1.5])
  if N == 1:
    DA = 0
  else:
    target = lighthouses[0]
    for source in lighthouses[1:int(len(lighthouses)/2)+1]:
      isValid, tang, line = get_illumination_line(source['center'], target['center'], placement_center, len(lighthouses))
      ax.add_line(line) 
      if isValid:
        ax.scatter(source['center'][0], source['center'][1], color="green")
        ax.scatter(tang[0], tang[1], color="green") 
        break
      else:
        ax.scatter(source['center'][0], source['center'][1], color="red")
        ax.scatter(tang[0], tang[1], color="red") 
    if source['center'][1] <= tang[1]:
      # The dark area is infinite
      DA = inf      
    else:
      # We can find the dark area
      coeff = np.polyfit([tang[0], source['center'][0]], [tang[1], source['center'][1]], 1) # finds the coefficients of y = ax + b for points x, y.
      target_cross_x = -coeff[1]/coeff[0] # we look for 0 = ax' + b --> x = -b/a
      ax.scatter(target_cross_x, 0.0, color="orange")
      ax.add_line(Line2D([tang[0], target_cross_x], [tang[1], 0.0], color='gray', linewidth=0.5))
      ax.add_line(Line2D([lighthouses[0]['center'][0], target_cross_x], [lighthouses[0]['center'][1], 0.0], color='gray', linewidth=0.5))
      x = dist_2d((target_cross_x, 0.0), tang) # this is the nugget, we can find the dark area from this.
      DA = N * (x - np.arctan(x)) # Theorem 4.3
      plt.xlim([-N-1.5, target_cross_x+1.5])

  DA_theorem = theorem_4_3_formula(N)
  print("D("+str(N)+") by Calculation:",DA)
  print("D("+str(N)+") by Theorem:",DA_theorem)
  
  ax.set_title(str(N)+" lighthouses")
  plt.show()
  return DA, DA_theorem

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

  plt.xlim([-N-1.5, N+1.5])
  plt.ylim([-N-1.5, N+1.5])
  if N == 1:
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
      DA = N * (x - np.arctan(x)) # Theorem 4.3
      plt.xlim([-N-1.5, target_cross_x+1.5])

  DA_theorem = theorem_4_3_formula(N)
  print("D("+str(N)+") by Calculation:",DA)
  print("D("+str(N)+") by Theorem:",DA_theorem)
  
  ax.set_title(str(N)+" lighthouses")
  plt.show() 
  return DA, DA_theorem
  
def compute_darkness(N, print_res=True):  
  if N == 1:
    DA = 0
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
    source, tangent, _ = get_first_illumination_line(lighthouses, placement_center)
    if source[1] <= tangent[1]:
      # The dark area is infinite
      DA = inf      
    else:
       # We can find the dark area
      coeff = np.polyfit([tangent[0], source[0]], [tangent[1], source[1]], 1) # finds the coefficients of y = ax + b for points x, y.
      target_cross_x = -coeff[1]/coeff[0] # we look for 0 = ax' + b --> x = -b/a 
      x = dist_2d((target_cross_x, 0.0), tangent) # this is the nugget, we can find the dark area from this.
      DA = N * (x - np.arctan(x)) # Theorem 4.3

  DA_theorem = theorem_4_3_formula(N)
  if print_res:
    print("D("+str(N)+") by Calculation:",DA)
    print("D("+str(N)+") by Theorem:",DA_theorem)
  return DA, DA_theorem

def plot_results(maxL):
  '''
  Plotting code from the notebook. Plot the results upto a given number of lighthouses.

  It does not include even numbers in the plot, as they are known to be inf.
  ''' 
  N_L = range(1,maxL+1)
  DA, DA_theorem = zip(*[compute_darkness(N, print_res=False) for N in N_L]) 
  fig = plt.figure()
  ax = plt.axes()
  ax.scatter(N_L[::2], DA_theorem[::2], c='green')
  ax.scatter(N_L[::2], DA[::2], c='blue')
  errs = [abs(DA[i]-DA_theorem[i]) for i in range(0, maxL, 2)]
  ax.scatter(N_L[::2], errs, c='red')
  ax.set_xlabel("Number of Lighthouses")
  ax.set_ylabel("Total Dark Area")
  plt.show()

if __name__ == "__main__":
  num_lighthouses = 9
  assert(num_lighthouses > 0)
  draw_all(num_lighthouses)
  #compute_darkness(num_lighthouses)
  #plot_results(500)
