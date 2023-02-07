from cq_server.ui import ui, show_object, debug
import cadquery as cq
from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCone


def generate_shape():
    shape = BRepPrimAPI_MakeSphere(1).Shape()
    return shape


def generate_shape_1(base):
    shape_1 = BRepPrimAPI_MakeCone(base, 0, 1, 3).Shape()


def generate_demo():
    Ball = generate_shape()
    Ball_and_Cone=generate_shape_1(Ball)
    return Ball_and_Cone


demo = generate_demo()
show_object(cq.Shape.cast(demo))
