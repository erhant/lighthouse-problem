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
  target = lighthouses[0] # this is the target
  
  # starting from the closest immediate lighthouse
  for i in range(1,int(len(lighthouses)/2)):
    print("I:",i)
    source = lighthouses[i]
    tang = find_tangent(source['left'], target['center']) # find tangent 
    j = 0
    coll = False

    # see if this ray collides with anything in between
    for j in range(i): 
      l = lighthouses[j]
      print("J:",j) 
      # y = px + q --> -px + y -q = 0
      if not checkCollision(source['left'][0], source['left'][1], tang[0], tang[1], l['center'][0], l['center'][1], 1.0):
        print("I",i,"does not collide with J",j)        
      else:
        print("I",i,"collides with J",j)
        coll = True
      j += 1
    
    if not coll:
      return source['left'], tang, Line2D([source['left'][0], tang[0]], [source['left'][1], tang[1]], color='green', linewidth=0.5)
    elif i+1 == int(len(lighthouses)/2):
      return source['left'], tang, Line2D([source['left'][0], tang[0]], [source['left'][1], tang[1]], color='red', linewidth=0.5)

def draw_match(N):
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

  source, tangent, illumline = get_first_illumination_line(lighthouses)
  ax.add_line(illumline)
  ax.scatter(source[0], source[1], color="green")
  ax.scatter(tangent[0], tangent[1], color="green")

  plt.xlim([-N-1.5, N+1.5])
  plt.ylim([-N-1.5, N+1.5])

  ax.set_title(str(N)+" lighthouses")
  plt.show()

if __name__ == "__main__":
  num_lighthouses = 13 # bug with 4...
  assert(num_lighthouses > 0)
  draw_match(num_lighthouses)
  