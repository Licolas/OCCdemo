from cq_server.ui import ui, show_object, debug
import cadquery as cq
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepFeat import BRepFeat_MakeCylindricalHole
from OCP.gp import gp_Dir, gp_Ax1, gp_Pnt, gp_Ax2


def generate_shape():
    basic_shape = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 0), 0.5).Shape()
    return basic_shape


def make_holes_1(base):
    feature_diameter = 0.2
    feature_origin = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    feature_maker = BRepFeat_MakeCylindricalHole()
    feature_maker.Init(base, feature_origin)
    feature_maker.Build()
    feature_maker.Perform(feature_diameter / 2.0)
    shape = feature_maker.Shape()
    return shape


def make_holes_2(base):
    feature_diameter = 0.2
    feature_origin = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0))
    feature_maker = BRepFeat_MakeCylindricalHole()
    feature_maker.Init(base, feature_origin)
    feature_maker.Build()
    feature_maker.Perform(feature_diameter / 2.0)
    shape = feature_maker.Shape()
    return shape


def make_holes_3(base):
    feature_diameter = 0.2
    feature_origin = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))
    feature_maker = BRepFeat_MakeCylindricalHole()
    feature_maker.Init(base, feature_origin)
    feature_maker.Build()
    feature_maker.Perform(feature_diameter / 2.0)
    shape = feature_maker.Shape()
    return shape


def generate_demo():
    basic_shape = generate_shape()
    basic_result1 = make_holes_1(basic_shape)
    basic_result2 = make_holes_2(basic_result1)
    basic_result3 = make_holes_3(basic_result2)
    return basic_result3


demo = generate_demo()
show_object(cq.Shape.cast(demo), options={'color': 'lightblue'})
