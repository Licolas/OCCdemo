from cq_server.ui import ui, show_object, debug
import cadquery as cq
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCone


def generate_shape():
    # 创建圆锥台
    R1 = 0.5
    R2 = 1
    Height = 0.8
    Cone = BRepPrimAPI_MakeCone(R1, R2, Height).Shape()
    return Cone


def generate_demo():
    basic_Shape = generate_shape()
    return basic_Shape


demo = generate_demo()
show_object(cq.Shape.cast(demo))
