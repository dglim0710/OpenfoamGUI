
import salome
salome.salome_init()

import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")

import SMESH
from salome.smesh import smeshBuilder
smesh = smeshBuilder.New(salome.myStudy)

# --- Define vertex and vector
partition_position = geompy.MakeVertex(0, 0, 0)
o = geompy.MakeVertex(0, 0, 0)
z = geompy.MakeVertex(0, 0, 1)
v = geompy.MakeVector(o, z)

# --- Define parameters
wafer_radius = 0.15
height = 0.0025
width = 0.011
length = 0.0004
trans = -0.0155

# --- Make a shape and create study
disk = geompy.MakeDiskR(wafer_radius, 1)
rectangle1 = geompy.MakeFaceHW(width, length, 1)
rectangle2 = geompy.MakeTranslation(rectangle1, trans, 0., 0.)

wafer = geompy.MakePartition([disk],[rectangle2])
id_wafer = geompy.addToStudy(wafer,"wafer")

group1 = geompy.CreateGroup(wafer, geompy.ShapeType['FACE'])
geompy.AddObject(group1, 15)
group2 = geompy.CreateGroup(wafer, geompy.ShapeType['FACE'])
geompy.AddObject(group2, 2)
group3 = geompy.CreateGroup(wafer, geompy.ShapeType['FACE'])
geompy.AddObject(group3, 2)
geompy.AddObject(group3, 15)
group4 = geompy.CreateGroup(wafer, geompy.ShapeType['EDGE'])
geompy.AddObject(group4, 12)
geompy.AddObject(group4, 7)
group5 = geompy.CreateGroup(wafer, geompy.ShapeType['EDGE'])
geompy.AddObject(group5, 14)
geompy.AddObject(group5, 10)
group6 = geompy.CreateGroup(wafer, geompy.ShapeType['EDGE'])
geompy.AddObject(group6, 4)

id_group1 = geompy.addToStudyInFather(wafer,group1, "rec")
id_group2 = geompy.addToStudyInFather(wafer,group2, "tri")
id_group3 = geompy.addToStudyInFather(wafer,group3, "bottom")
id_group4 = geompy.addToStudyInFather(wafer,group4, 'long')
id_group5 = geompy.addToStudyInFather(wafer,group5, 'short')
id_group7 = geompy.addToStudyInFather(wafer,group6, 'outlet')

# --- Generate a mesh

wafer = smesh.Mesh(wafer, "wafer")
algo1D = wafer.Segment()
algo1D.MaxSize(length=height)
algo2D = wafer.Triangle(smeshBuilder.NETGEN_2D)

longSeg = 55
shortSeg1 = 10
shortSeg2 = shortSeg1/2 

subMeshRec = wafer.Quadrangle(group1)
subMeshRec1D_long = wafer.Segment(group4)
subMeshRec1D_long.NumberOfSegments(longSeg)
subMeshRec1D_short1 = wafer.Segment(group5)
subMeshRec1D_short1.NumberOfSegments(shortSeg1)
#subMeshRec1D_short2 = wafer.Segment(group6)
#subMeshRec1D_short2.NumberOfSegments(shortSeg2)

wafer.Compute()

aSmeshGroup1 = wafer.GroupOnGeom(group3, "bottom")
aSmeshGroup2 = wafer.GroupOnGeom(group6, "outlet_edge")

obj = wafer
StepSize = height
nbSteps = 1
wafer.ExtrusionByNormal(obj, height, nbSteps, MakeGroups=True)

wafer_Groups = wafer.GetGroups()
wafer_GroupName = wafer.GetGroupNames()

for i in range(0,len(wafer_GroupName)):
    if wafer_GroupName[i] == 'bottom_extruded' or wafer_GroupName[i] == 'outlet_edge' or wafer_GroupName[i] == 'outlet_edge_top':
        wafer.RemoveGroup(wafer_Groups[i])
    if wafer_GroupName[i] == 'bottom_top':
        smesh.SetName(wafer_Groups[i], 'top')
    elif wafer_GroupName[i] == 'outlet_edge_extruded':
        smesh.SetName(wafer_Groups[i], 'outlet')

#wafer.ExportUNV('C:/Users/user/Desktop/Project/0501/OpenfoamGUI-master/Case/Mesh_Tri2.unv')

#import os
#os._exit(0)



