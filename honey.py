import rhinoscriptsyntax as rs
import random
import voronoi

def randomPoint():
	return (random.randrange(10), random.randrange(10), 0)

# The voronoi module wants its points as objects, instead of just tuples
class Point(object):
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

points = []
for i in range(10):
	point = Point(random.randrange(10), random.randrange(10), 0)
	rs.AddPoint(point.x, point.y, point.z)
	points.append(point)
results = voronoi.computeVoronoiDiagram(points)
rs.MessageBox(results)


circle = rs.AddCircle3Pt(randomPoint(), randomPoint(), randomPoint())
center = rs.CircleCenterPoint(circle)
rs.AddCircle(center, 1)