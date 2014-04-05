import rhinoscriptsyntax as rs
import honey



points = rs.GetObjects ( message="Select points, or none for random...", filter=1, preselect=True)
if not points:
	points = honey.randomPoints(10,40)
mode = rs.GetBoolean (message="Voronoi diagram or Delaunay triangulation?", items=[["Mode", "Voronoi", "Delaunay"]], defaults=[False])
if mode:
	if mode[0] is False:
		honey.plotVoronoi(points)
	elif mode[0] is True:
		honey.plotDelaunay(points)
	else:
		print mode[0]
