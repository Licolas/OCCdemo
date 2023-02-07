from OCP.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir, gp_Circ, gp_Ax2
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.BRepOffsetAPI import BRepOffsetAPI_MakePipe
import cadquery as cq
from cq_server.ui import ui, show_object

e1 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, 10)).Edge()
w1 = BRepBuilderAPI_MakeWire(e1)

c2 = gp_Circ(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 1)), 1)
e2 = BRepBuilderAPI_MakeEdge(c2).Edge()
w2 = BRepBuilderAPI_MakeWire(e2)
f2 = BRepBuilderAPI_MakeFace(w2.Wire())

s1 = BRepOffsetAPI_MakePipe(w1.Wire(), f2.Shape()).Shape()

show_object(cq.Shape.cast(s1))
