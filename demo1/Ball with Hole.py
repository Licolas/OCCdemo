from cq_server.ui import ui, show_object, debug
import cadquery as cq
from math import atan, cos, sin, pi
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform, BRepBuilderAPI_MakeWire, \
    BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace
from OCP.BRepFeat import BRepFeat_MakeCylindricalHole
from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder, \
    BRepPrimAPI_MakeTorus, BRepPrimAPI_MakeRevol
from OCP.TColgp import TColgp_Array1OfPnt
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Ax1, gp_Trsf, gp_Vec


def generate_shape():
    # 创建球台体
    sphere_radius = 1.0
    sphere_origin = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))    # 一个坐标系
    sphere = BRepPrimAPI_MakeSphere(sphere_origin, sphere_radius).Shape()
    return sphere


def add_feature(base):
    # 在球台体基础上添加中间的孔特征
    feature_diameter = 0.8
    feature_origin = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))   # 一个轴
    feature_maker = BRepFeat_MakeCylindricalHole()
    feature_maker.Init(base, feature_origin)
    feature_maker.Build()
    feature_maker.Perform(feature_diameter / 2.0)
    shape = feature_maker.Shape()
    return shape


def generate_demo():
    basic_shape = generate_shape()
    featured_shape = add_feature(basic_shape)
    return featured_shape


demo = generate_demo()
show_object(cq.Shape.cast(demo))
