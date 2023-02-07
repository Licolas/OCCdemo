from cq_server.ui import ui, show_object, debug
import cadquery as cq

from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, \
    BRepBuilderAPI_MakeShape
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir

E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(20, 0, 0)).Edge()
E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(20, 0, 0), gp_Pnt(20, 10, 0)).Edge()
E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(20, 10, 0), gp_Pnt(15, 15, 0)).Edge()
E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(15, 15, 0), gp_Pnt(0, 15, 0)).Edge()
E15 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 15, 0), gp_Pnt(0, 0, 0)).Edge()
W1 = BRepBuilderAPI_MakeWire(E11, E12, E13, E14)
# W2 = BRepBuilderAPI_MakeWire(E15)
# W1 = BRepBuilderAPI_MakeWire.Add(W1, E15)
W1.Add(E15)

F1 = BRepBuilderAPI_MakeFace(W1.Wire())

S = BRepPrimAPI_MakePrism(F1.Face(), gp_Vec(0, 0, 10)).Shape()

show_object(cq.Shape.cast(S), options={'color': 'pink'})
