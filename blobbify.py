import rhinoscriptsyntax as rs
import honey


curves = rs.GetObjects ( message="Select curves to be blobbified...", filter=4)
honey.makeCurvesBlobby(curves, 1)