import rhinoscriptsyntax as rs
import honey

curves = rs.GetObjects ( message="Select curves to be blobbified...", filter=4)
radius = rs.GetReal ( message="Enter endpoint radius:", number=1.0 )

honey.makeCurvesBlobby(curves, radius)