from OCP.GeomAPI import GeomAPI_Interpolate
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Circ, gp_Elips, gp_Vec
from OCP.GC import GC_MakeSegment, GC_MakeCircle, GC_MakeArcOfCircle, GC_MakeEllipse
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeSweep
import cadquery as cq
from cq_server.ui import ui, show_object
from OCP.BRepOffsetAPI import BRepOffsetAPI_MakePipe


# 函数作用：通过圆心和半径和角度生成圆弧
# 输入：圆心坐标，半径值，角度值
# 输出：暂定只输出圆弧
def generate_sweep_line():
    Location = gp_Pnt(0, 0, 0)
    Axis = gp_Dir(0, 0, 1)
    CircleAxis = gp_Ax2(Location, Axis)
    Circle = gp_Circ(CircleAxis, 10)
    ArcofCircle0 = GC_MakeArcOfCircle(Circle, 0 / 180 * 3.14, 90 / 180 * 3.14, True)
    ArcofCircle1 = BRepBuilderAPI_MakeEdge(ArcofCircle0.Value())
    ArcofCircle = BRepBuilderAPI_MakeWire(ArcofCircle1.Edge())
    return ArcofCircle


def generate_sweep_shape():
    e1 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, 1)).Edge()
    e2 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 1), gp_Pnt(0, 0.5, 1)).Edge()
    e3 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0.5, 1), gp_Pnt(0, 1, 0)).Edge()
    e4 = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 1, 0), gp_Pnt(0, 0, 0)).Edge()
    w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, e4).Wire()
    f1 = BRepBuilderAPI_MakeFace(w1)
    return f1


sweep1 = generate_sweep_line()
shape1 = generate_sweep_shape()

s = BRepOffsetAPI_MakePipe(sweep1.Wire(), shape1.Shape()).Shape()

show_object(cq.Shape.cast(s), options={'color': 'green'})
