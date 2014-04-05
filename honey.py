import rhinoscriptsyntax as rs
import random
import voronoi

from decimal import *
getcontext().prec = 7
# need python code to have same precision as Rhino

# The voronoi library expects points to have (lowercase) x,y,z properties, whereas rhino gives them uppercase
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

def randomPoints(quantity, area):
	points = []
	for i in range(quantity):
		x = random.randrange(area)
		y = random.randrange(area)
		z = 0
		point = rs.AddPoint(x, y, z)
		points.append(point)
	return points

def preparePoints(rspoints):
	lowerpoints = []
	for point in rspoints:
		coord = rs.PointCoordinates(point)
		newpoint = Point(coord.X, coord.Y, coord.Z)
		print dir(newpoint)
		lowerpoints.append(newpoint)	
	return lowerpoints

def plotVoronoi(points):
	results = voronoi.computeVoronoiDiagram(preparePoints(points))
	curves = []
	print "number of edges: "+str(len(results[2]))
	for edge in results[2]:
		if edge[1] != -1 and edge[2] != -1:
			startx = decimate(results[0][edge[1]][0])
			starty = decimate(results[0][edge[1]][1])
			endx = decimate(results[0][edge[2]][0])
			endy = decimate(results[0][edge[2]][1])
			startpoint = [startx, starty, 0]
			endpoint = [endx, endy, 0]
			curves.append(rs.AddLine(startpoint, endpoint))
	return curves

def plotDelaunay(points):
	results = voronoi.computeDelaunayTriangulation(preparePoints(points))
	curves = []
	for result in results:
		curves.append(rs.AddLine([points[result[0]].x, points[result[0]].y, 0], [points[result[1]].x, points[result[1]].y, 0]))
		curves.append(rs.AddLine([points[result[1]].x, points[result[1]].y, 0], [points[result[2]].x, points[result[2]].y, 0]))
		curves.append(rs.AddLine([points[result[2]].x, points[result[2]].y, 0], [points[result[0]].x, points[result[0]].y, 0]))
	return curves

def makeCurvesBlobby(curves, vertex_radius):
	existingsegments = []
	for curve in curves:
		curvelength = rs.CurveLength(curve)
		attenuation = lerp(curvelength, 0.0, 20.0, vertex_radius-vertex_radius/6, vertex_radius/2)
		if attenuation < vertex_radius/3:
			attenuation = vertex_radius/3
		# rhinoscriptsyntax.AddPipe (curve_id, parameters, radii, blend_type=0, cap=0, fit=False)
		pipe = rs.AddPipe(curve, (0,0.5,1), (vertex_radius, attenuation, vertex_radius), fit=True)
		startsphere = rs.AddSphere(rs.CurveStartPoint(curve), vertex_radius)
		endsphere = rs.AddSphere(rs.CurveEndPoint(curve), vertex_radius)
		if pipe and startsphere and endsphere:
			pipe = rs.BooleanUnion([startsphere, pipe, endsphere], True)
	web = rs.JoinSurfaces(existingsegments, True)
	return web
