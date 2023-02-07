from cq_server.ui import ui, show_object, debug
import cadquery as cq

from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCP.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir

E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(100, 0, 0)).Edge()
E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(100, 0, 0), gp_Pnt(100, 100, 0)).Edge()
E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(100, 100, 0), gp_Pnt(0, 100, 0)).Edge()
E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 100, 0), gp_Pnt(0, 0, 0)).Edge()
W1 = BRepBuilderAPI_MakeWire(E11, E12, E13, E14)

S = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(W1.Wire()).Face(), gp_Vec(0, 0, 50)).Shape()

show_object(cq.Shape.cast(S), options={'color': 'pink'})
