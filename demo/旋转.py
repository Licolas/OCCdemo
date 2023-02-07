from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Vec, gp_Ax1
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
import cadquery as cq
from cq_server.ui import ui, show_object

e1 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(5, 5, 0)).Edge()
e2 = BRepBuilderAPI_MakeEdge(gp_Pnt(5, 5, 0), gp_Pnt(5, 10, 0)).Edge()
e3 = BRepBuilderAPI_MakeEdge(gp_Pnt(5, 10, 0), gp_Pnt(0, 15, 0)).Edge()
e4 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 15, 0), gp_Pnt(0, 0, 0)).Edge()

w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)

s = BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(w1.Wire()).Face(), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0))).Shape()

show_object(cq.Shape.cast(s), options={'color': 'pink'})
