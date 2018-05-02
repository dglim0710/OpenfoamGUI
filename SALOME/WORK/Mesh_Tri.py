
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
height = 0.0001

# --- Make a shape and create study
wafer = geompy.MakeDiskR(wafer_radius, 1)

id_wafer = geompy.addToStudy(wafer,"wafer")

group1 = geompy.CreateGroup(wafer, geompy.ShapeType["FACE"])
geompy.AddObject(group1,1)
group2 = geompy.CreateGroup(wafer, geompy.ShapeType["EDGE"])
geompy.AddObject(group2,3)

id_group1 = geompy.addToStudyInFather(wafer,group1, "bottom")
id_group2 = geompy.addToStudyInFather(wafer,group2, "outlet")


# --- Generate a mesh

wafer = smesh.Mesh(wafer, "wafer")
algo1D = wafer.Segment()
algo1D.MaxSize(length=height)
algo2D = wafer.Triangle(smeshBuilder.NETGEN_2D)

wafer.Compute()
aSmeshGroup1 = wafer.GroupOnGeom(group1, "bottom")
aSmeshGroup2 = wafer.GroupOnGeom(group2, "outlet_edge")

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

wafer.ExportUNV('/home/daegyu/Work/OpenfoamGUI/Case/Mesh_Tri.unv')

import os
os._exit(0)
    