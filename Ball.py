from cq_server.ui import ui, show_object, debug
import cadquery as cq
from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere


def generate_shape():
    shape = BRepPrimAPI_MakeSphere(1).Shape()
    return shape


def generate_demo():
    Ball = generate_shape()
    return Ball


demo = generate_demo()
show_object(cq.Shape.cast(demo), options={'color': 'green'})
