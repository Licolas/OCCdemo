import cadquery as cq
from cq_server.ui import ui, show_object
from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Pln, gp_Ax3


def generate_object():
    radius = 0.5
    origin = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    origin_object = BRepPrimAPI_MakeSphere(origin, radius, 90/180*3.14).Shape()
    return origin_object


def generate_demo():
    basic_Shape = generate_object()
    return basic_Shape


demo = generate_demo()
show_object(cq.Shape.cast(demo), options={'color': 'lightblue'})
