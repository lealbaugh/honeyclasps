import rhinoscriptsyntax as rs
import random
import voronoi

from decimal import *
getcontext().prec = 7
# need python code to have same precision as Rhino


vertex_radius = 1.5

# The voronoi module wants its points as objects, instead of just tuples
class Point(object):
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

def lerp(value, inputLow, inputHigh, outputLow, outputHigh):
	return (((value-inputLow)/(inputHigh-inputLow))*(outputHigh-outputLow))+outputLow

def decimate(input): 
	# output a Decimal at rhino-compatible amounts of precision
	return Decimal(input).quantize(Decimal('1.000'))

def makePipesFromVoronoi(results):
	for edge in results[2]:
		if edge[1] != -1 and edge[2] != -1:
			startx = decimate(results[0][edge[1]][0])
			starty = decimate(results[0][edge[1]][1])
			endx = decimate(results[0][edge[2]][0])
			endy = decimate(results[0][edge[2]][1])
			startpoint = [startx, starty, 0]
			endpoint = [endx, endy, 0]
			curvelength = rs.Distance(startpoint, endpoint)
			if curvelength < 25:
				drawPipe(startpoint, endpoint, curvelength)
	# for vertex in results[0]:
	# 	rs.AddSphere((vertex[0],vertex[1],0), vertex_radius)

def makePipesFromDelauney(points, results):
	for result in results:
		drawPipe(points[result[0]].x, points[result[0]].y, points[result[1]].x, points[result[1]].y)
		drawPipe(points[result[1]].x, points[result[1]].y, points[result[2]].x, points[result[2]].y)
		drawPipe(points[result[2]].x, points[result[2]].y, points[result[0]].x, points[result[0]].y)
	for vertex in points:
		rs.AddSphere((vertex.x,vertex.y,0), vertex_radius)


def drawPipe(startpoint, endpoint, curvelength):
	curve = rs.AddLine(startpoint, endpoint)
	attenuation = lerp(curvelength, 0.0, 20.0, vertex_radius-vertex_radius/6, vertex_radius/2)
	if attenuation < vertex_radius/3:
		attenuation = vertex_radius/3
	# rhinoscriptsyntax.AddPipe (curve_id, parameters, radii, blend_type=0, cap=0, fit=False)
	pipe = rs.AddPipe(curve, (0,0.5,1), (vertex_radius, attenuation, vertex_radius), fit=True)
	startsphere = rs.AddSphere(startpoint, vertex_radius)
	endsphere = rs.AddSphere(endpoint, vertex_radius)
	if pipe and startsphere and endsphere:
		pipe = rs.BooleanUnion([startsphere, pipe, endsphere], True)
	return pipe

points = []
for i in range(30):
	point = Point(random.randrange(20), random.randrange(20), 0)
	# rs.AddPoint(point.x, point.y, point.z)
	points.append(point)

makePipesFromVoronoi(voronoi.computeVoronoiDiagram(points))
# makePipesFromDelauney(points, voronoi.computeDelaunayTriangulation(points))