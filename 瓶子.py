import math

from OCC.Core.gp import gp_Pnt, gp_OX, gp_Vec, gp_Trsf, gp_DZ, gp_Ax2, gp_Ax3, gp_Pnt2d, gp_Dir2d, gp_Ax2d
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.GCE2d import GCE2d_MakeSegment
from OCC.Core.Geom import Geom_Plane, Geom_CylindricalSurface
from OCC.Core.Geom2d import Geom2d_Ellipse, Geom2d_TrimmedCurve
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeThickSolid, BRepOffsetAPI_ThruSections
from OCC.Core.BRepLib import breplib
from OCC.Core.BRep import BRep_Tool_Surface, BRep_Builder
from OCC.Core.TopoDS import topods, TopoDS_Compound
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Display.OCCViewer import rgb_color


def face_is_plane(face):
    """
    Returns True if the TopoDS_Shape is a plane, False otherwise
    """
    hs = BRep_Tool_Surface(face)  # Returns the geometric surface of the face.
    downcast_result = Geom_Plane.DownCast(hs)
    # The handle is null if downcast failed or is not possible, that is to say the face is not a plane
    if downcast_result is None:
        return False
    else:
        return True


def geom_plane_from_face(aFace):
    """
    Returns the geometric(几何的) plane entity from a planar(平面的，二维的) surface
    """
    return Geom_Plane.DownCast(BRep_Tool_Surface(aFace))


height = 70
width = 50
thickness = 30

print("creating bottle")
# The points we'll use to create the profile of the bottle's body
aPnt1 = gp_Pnt(-width / 2.0, 0, 0)
aPnt2 = gp_Pnt(-width / 2.0, -thickness / 4.0, 0)
aPnt3 = gp_Pnt(0, -thickness / 2.0, 0)
aPnt4 = gp_Pnt(width / 2.0, -thickness / 4.0, 0)
aPnt5 = gp_Pnt(width / 2.0, 0, 0)

aArcOfCircle = GC_MakeArcOfCircle(aPnt2, aPnt3, aPnt4)
'新思路，三点做圆弧，没试过'
aSegment1 = GC_MakeSegment(aPnt1, aPnt2)
aSegment2 = GC_MakeSegment(aPnt4, aPnt5)

# Could also construct the line edges directly using the points instead of the resulting line
aEdge1 = BRepBuilderAPI_MakeEdge(aSegment1.Value())
aEdge2 = BRepBuilderAPI_MakeEdge(aArcOfCircle.Value())
aEdge3 = BRepBuilderAPI_MakeEdge(aSegment2.Value())

# Create a wire out of the edges
aWire = BRepBuilderAPI_MakeWire(aEdge1.Edge(), aEdge2.Edge(), aEdge3.Edge())

# Quick way to specify(明确指出) the X axis
xAxis = gp_OX()
'gp_OX是用来确定x轴的'

# Set up the mirror
aTrsf = gp_Trsf()
'Returns the identity transformation(恒等变换).'
aTrsf.SetMirror(xAxis)
'Makes the transformation into a symmetrical transformation(对称变换). p is the center of the symmetry.'

# Apply the mirror transformation
aBRespTrsf = BRepBuilderAPI_Transform(aWire.Wire(), aTrsf)
'''
BRepBuilderAPI_Transform()

Constructs a framework(框架) for applying the geometric transformation t to a shape. 
Use the function perform to define the shape to transform.
'''

# Get the mirrored shape back out of the transformation and convert back to a wire
aMirroredShape = aBRespTrsf.Shape()

# A wire instead of a generic shape now
aMirroredWire = topods.Wire(aMirroredShape)
'''
topods.Wire()

Casts shape s to the more specialized return type.
wire. exceptions standard_typemismatch if s cannot be cast to this return type.
'''

# Combine the two constituent wires
mkWire = BRepBuilderAPI_MakeWire()  # 空线条
mkWire.Add(aWire.Wire())  # 往空线条上添加线条
mkWire.Add(aMirroredWire)
myWireProfile = mkWire.Wire()

# The face that we'll sweep to make the prism
myFaceProfile = BRepBuilderAPI_MakeFace(myWireProfile)  # 根据Wire创建一个Face

# We want to sweep the face along the Z axis to the height
aPrismVec = gp_Vec(0, 0, height)
myBody = BRepPrimAPI_MakePrism(myFaceProfile.Face(), aPrismVec)
'到这里已经都会了！'

# Add fillets to all edges through the explorer
mkFillet = BRepFilletAPI_MakeFillet(myBody.Shape())
'BRepFilletAPI_MakeFillet()'
anEdgeExplorer = TopExp_Explorer(myBody.Shape(), TopAbs_EDGE)
'''
TopExp_Explorer
Creates an empty explorer, becomes usefull after init.
'''

while anEdgeExplorer.More():
    anEdge = topods.Edge(anEdgeExplorer.Current())
    mkFillet.Add(thickness / 12.0, anEdge)

    anEdgeExplorer.Next()

myBody = mkFillet

# Create the neck of the bottle
neckLocation = gp_Pnt(0, 0, height)
neckAxis = gp_DZ()
'''
gp_DZ()
Returns a unit vector with the combination (0,0,1).
'''
neckAx2 = gp_Ax2(neckLocation, neckAxis)

myNeckRadius = thickness / 4.0
myNeckHeight = height / 10.0

mkCylinder = BRepPrimAPI_MakeCylinder(neckAx2, myNeckRadius, myNeckHeight)

myBody = BRepAlgoAPI_Fuse(myBody.Shape(), mkCylinder.Shape())
'''
BRepAlgoAPI_Fuse()
将两个实体构造成一个实体。
'''

# Our goal is to find the highest Z face and remove it
faceToRemove = None
'''什么意思？？faceToRemove'''
zMax = -1

# We have to work our way through all the faces to find the highest Z face, so we can remove it for the shell
aFaceExplorer = TopExp_Explorer(myBody.Shape(), TopAbs_FACE)
while aFaceExplorer.More():  # Returns true if there are more shapes in the exploration.
    aFace = topods.Face(aFaceExplorer.Current())

    if face_is_plane(aFace):
        aPlane = geom_plane_from_face(aFace)

        # We want the highest Z face, so compare this to the previous faces
        aPnt = aPlane.Location()
        aZ = aPnt.Z()
        if aZ > zMax:
            zMax = aZ
            faceToRemove = aFace

    aFaceExplorer.Next()

facesToRemove = TopTools_ListOfShape()
facesToRemove.Append(faceToRemove)

myBody = BRepOffsetAPI_MakeThickSolid(myBody.Shape(), facesToRemove, -thickness / 50.0, 0.001)

# Set up our surfaces for the threading on the neck
neckAx2_Ax3 = gp_Ax3(neckLocation, gp_DZ())
aCyl1 = Geom_CylindricalSurface(neckAx2_Ax3, myNeckRadius * 0.99)
aCyl2 = Geom_CylindricalSurface(neckAx2_Ax3, myNeckRadius * 1.05)

# Set up the curves for the threads on the bottle's neck
aPnt = gp_Pnt2d(2.0 * math.pi, myNeckHeight / 2.0)
aDir = gp_Dir2d(2.0 * math.pi, myNeckHeight / 4.0)
anAx2d = gp_Ax2d(aPnt, aDir)

aMajor = 2.0 * math.pi
aMinor = myNeckHeight / 10.0

anEllipse1 = Geom2d_Ellipse(anAx2d, aMajor, aMinor)
anEllipse2 = Geom2d_Ellipse(anAx2d, aMajor, aMinor / 4.0)

anArc1 = Geom2d_TrimmedCurve(anEllipse1, 0, math.pi)
anArc2 = Geom2d_TrimmedCurve(anEllipse2, 0, math.pi)

anEllipsePnt1 = anEllipse1.Value(0)
anEllipsePnt2 = anEllipse1.Value(math.pi)

aSegment = GCE2d_MakeSegment(anEllipsePnt1, anEllipsePnt2)

# Build edges and wires for threading
anEdge1OnSurf1 = BRepBuilderAPI_MakeEdge(anArc1, aCyl1)
anEdge2OnSurf1 = BRepBuilderAPI_MakeEdge(aSegment.Value(), aCyl1)
anEdge1OnSurf2 = BRepBuilderAPI_MakeEdge(anArc2, aCyl2)
anEdge2OnSurf2 = BRepBuilderAPI_MakeEdge(aSegment.Value(), aCyl2)

threadingWire1 = BRepBuilderAPI_MakeWire(anEdge1OnSurf1.Edge(), anEdge2OnSurf1.Edge())
threadingWire2 = BRepBuilderAPI_MakeWire(anEdge1OnSurf2.Edge(), anEdge2OnSurf2.Edge())

# Compute the 3D representations of the edges/wires
breplib.BuildCurves3d(threadingWire1.Shape())
breplib.BuildCurves3d(threadingWire2.Shape())

# Create the surfaces of the threading
aTool = BRepOffsetAPI_ThruSections(True)
aTool.AddWire(threadingWire1.Wire())
aTool.AddWire(threadingWire2.Wire())
aTool.CheckCompatibility(False)
myThreading = aTool.Shape()

# Build the resulting compound
bottle = TopoDS_Compound()
aBuilder = BRep_Builder()
aBuilder.MakeCompound(bottle)
aBuilder.Add(bottle, myBody.Shape())
aBuilder.Add(bottle, myThreading)
print("bottle finished")

if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayColoredShape(bottle, update=True, color=rgb_color(0.1, 0.5, 0))
    start_display()
