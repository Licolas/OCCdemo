from OCP.GC import GC_MakeCircle
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Vec
import cadquery as cq
from cq_server.ui import ui, show_object
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace,BRepBuilderAPI_MakeEdge,BRepBuilderAPI_MakeWire

C1 = GC_MakeCircle(gp_Ax2(gp_Pnt(0, 0, 5), gp_Dir(0, 0, -1)), 8).Value()
e1=BRepBuilderAPI_MakeEdge(C1).Edge()
w1=BRepBuilderAPI_MakeWire(e1)

S = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(w1.Wire()).Face(), gp_Vec(0, 0, 10)).Shape()

show_object(cq.Shape.cast(S))
