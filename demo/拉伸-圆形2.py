from cq_server.ui import ui, show_object, debug
import cadquery as cq
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCP.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax2, gp_Circ

origin = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
C1 = gp_Circ(origin, 5)

origin1 = gp_Ax2(gp_Pnt(0, 7, 0), gp_Dir(0, 0, 1))
C2 = gp_Circ(origin1, 2)

e1 = BRepBuilderAPI_MakeEdge(C1).Edge()
e2 = BRepBuilderAPI_MakeEdge(C2).Edge()

w1 = BRepBuilderAPI_MakeWire(e1)
w2 = BRepBuilderAPI_MakeWire(e2)

S1 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(w1.Wire()).Face(), gp_Vec(0, 0, 5)).Shape()
S2 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(w2.Wire()).Face(), gp_Vec(0, 0, 5)).Shape()


show_object(cq.Shape.cast(S1), options={'color': 'pink'})
show_object(cq.Shape.cast(S2), options={'color': 'yellow'})

