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

def makePipesFromVoronoi(results):
	for edge in results[2]:
		if edge[1] != -1 and edge[2] != -1:
			startx = results[0][edge[1]][0]
			starty = results[0][edge[1]][1]
			endx = results[0][edge[2]][0]
			endy = results[0][edge[2]][1]
			drawPipe(startx, starty, endx, endy)
	for vertex in results[0]:
		rs.AddSphere((vertex[0],vertex[1],0), vertex_radius)

def makePipesFromDelauney(points, results):
	for result in results:
		drawPipe(points[result[0]].x, points[result[0]].y, points[result[1]].x, points[result[1]].y)
		drawPipe(points[result[1]].x, points[result[1]].y, points[result[2]].x, points[result[2]].y)
		drawPipe(points[result[2]].x, points[result[2]].y, points[result[0]].x, points[result[0]].y)
	for vertex in points:
		rs.AddSphere((vertex.x,vertex.y,0), vertex_radius)


def drawPipe(startx, starty, endx, endy):
	curve = rs.AddLine((startx, starty, 0), (endx, endy, 0))
	curvelength = rs.Distance((startx, starty, 0), (endx, endy, 0))
	attenuation = lerp(curvelength, 0.0, 20.0, vertex_radius, vertex_radius/3)
	if attenuation < vertex_radius/3:
		attenuation = vertex_radius/3
	# rhinoscriptsyntax.AddPipe (curve_id, parameters, radii, blend_type=0, cap=0, fit=False)
	rs.AddPipe(curve, (0,0.5,1), (vertex_radius, attenuation, vertex_radius), fit=True)

points = []
for i in range(30):
	point = Point(random.randrange(30), random.randrange(30), 0)
	rs.AddPoint(point.x, point.y, point.z)
	points.append(point)

# makePipesFromVoronoi(voronoi.computeVoronoiDiagram(points))
makePipesFromDelauney(points, voronoi.computeDelaunayTriangulation(points))