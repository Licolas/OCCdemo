from cq_server.ui import ui, show_object, debug
import cadquery as cq
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox


def generate_shape():
    Box = BRepPrimAPI_MakeBox(1,2,3).Shape()
    return Box



def generate_demo():
    Box=generate_shape()
    return Box


demo = generate_demo()
show_object(cq.Shape.cast(demo))