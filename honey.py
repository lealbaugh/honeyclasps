import rhinoscriptsyntax as rs
import random
import voronoi

vertex_radius = 1.5

# The voronoi module wants its points as objects, instead of just tuples
class Point(object):
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

def lerp(value, inputLow, inputHigh, outputLow, outputHigh):
	return (((value-inputLow)/(inputHigh-inputLow))*(outputHigh-outputLow))+outputLow

points = []
for i in range(30):
	point = Point(random.randrange(30), random.randrange(30), 0)
	rs.AddPoint(point.x, point.y, point.z)
	points.append(point)
results = voronoi.computeVoronoiDiagram(points)

for edge in results[2]:
	if edge[1] != -1 and edge[2] != -1:
		startx = results[0][edge[1]][0]
		starty = results[0][edge[1]][1]
		endx = results[0][edge[2]][0]
		endy = results[0][edge[2]][1]
		curve = rs.AddLine((startx, starty, 0), (endx, endy, 0))
		curvelength = rs.Distance((startx, starty, 0), (endx, endy, 0))
		attenuation = lerp(curvelength, 0.0, 20.0, vertex_radius, vertex_radius/3)
		if attenuation < vertex_radius/3:
			attenuation = vertex_radius/3
		# rhinoscriptsyntax.AddPipe (curve_id, parameters, radii, blend_type=0, cap=0, fit=False)
		rs.AddPipe(curve, (0,0.5,1), (vertex_radius, attenuation, vertex_radius), fit=True)
for vertex in results[0]:
	rs.AddSphere((vertex[0],vertex[1],0), vertex_radius)

	#        Returns a 3-tuple of:
	#
	#           (1) a list of 2-tuples, which are the x,y coordinates of the 
	#               Voronoi diagram vertices
	#           (2) a list of 3-tuples (a,b,c) which are the equations of the
	#               lines in the Voronoi diagram: a*x + b*y = c
	#           (3) a list of 3-tuples, (l, v1, v2) representing edges of the 
	#               Voronoi diagram.  l is the index of the line, v1 and v2 are
	#               the indices of the vetices at the end of the edge.  If 
	#               v1 or v2 is -1, the line extends to infinity.

# rs.MessageBox(results)
