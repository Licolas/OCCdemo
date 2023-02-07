from OCP.gp import gp_Pnt, gp_Vec
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
import cadquery as cq
from cq_server.ui import ui, show_object

e1 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(0, 5, 0)).Edge()
e2 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(0, -5, 0)).Edge()
e3 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(5, 0, 0)).Edge()
e4 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(-5, 0, 0)).Edge()
w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)

s = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(w1.Wire()).Face(), gp_Vec(0, 0, 5)).Shape()

show_object(cq.Shape.cast(s))
