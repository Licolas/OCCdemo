from cq_server.ui import ui, show_object, debug
import cadquery as cq
from OCP.GCE2d import GCE2d_MakeCircle
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCP.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax2, gp_Circ

origin = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
radius = 5
C1 = gp_Circ(origin, radius)
e1 = BRepBuilderAPI_MakeEdge(C1).Edge()
w1 = BRepBuilderAPI_MakeWire(e1)

S = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(w1.Wire()).Face(), gp_Vec(0, 0, 5)).Shape()

show_object(cq.Shape.cast(S), options={'color': 'pink'})
