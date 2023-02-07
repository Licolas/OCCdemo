from OCP.GeomAPI import GeomAPI_Interpolate
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Circ, gp_Elips, gp_Vec
from OCP.GC import GC_MakeSegment, GC_MakeCircle, GC_MakeArcOfCircle, GC_MakeEllipse
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
import cadquery as cq
from cq_server.ui import ui, show_object

# 函数作用：通过圆心和半径和角度生成圆弧
# 输入：圆心坐标，半径值，角度值
# 输出：暂定只输出圆弧
Location = gp_Pnt(0, 0, 0)
Axis = gp_Dir(0, 0, -1)
CircleAxis = gp_Ax2(Location, Axis)
Circle = gp_Circ(CircleAxis, 5)
ArcofCircle0 = GC_MakeArcOfCircle(Circle, 0 / 180 * 3.14, 180 / 180 * 3.14, True)
ArcofCircle1 = BRepBuilderAPI_MakeEdge(ArcofCircle0.Value())
ArcofCircle = BRepBuilderAPI_MakeWire(ArcofCircle1.Edge())

s = BRepPrimAPI_MakePrism(ArcofCircle.Wire(), gp_Vec(0, 0, 1)).Shape()

show_object(cq.Shape.cast(s), options={'color': 'blue'})
