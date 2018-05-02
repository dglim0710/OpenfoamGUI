from string import Template
import globalvar


def mesh_save(parsed):
    mesh_script = Template(r'''
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
height = $Mesh_size

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

wafer.ExportUNV('$Case_folder_path/Mesh_Tri.unv')

import os
os._exit(0)
    ''')
    builded = mesh_script.substitute(Mesh_size=parsed['Mesh_size'], Case_folder_path=globalvar.Case_folder_path)
    return builded


def transportProperties_save(parsed):
    transportProperties = Template(r'''
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | foam-extend: Open Source CFD                    |
|  \\    /   O peration     | Version:     4.0                                |
|   \\  /    A nd           | Web:         http://www.foam-extend.org         |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      transportProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

phase1
{
	transportModel	Newtonian;
	nu nu [0 2 -1 0 0 0 0] $Liquid_nu;
	rho rho [ 1 -3  0 0 0 0 0 ] $Liquid_Density;
}

phase2
{
	transportModel Newtonian;
	nu nu [0 2 -1 0 0 0 0] $Gas_nu;
	rho rho [ 1 -3  0 0 0 0 0 ] $Gas_Density;
}

mug mug [1 -1 -1 0 0 0 0] $Gas_Viscosity;
mul mul [1 -1 -1 0 0 0 0] $Liquid_Viscosity;

rhog rhog [ 1 -3  0 0 0 0 0 ] $Gas_Density;
rhol rhol [ 1 -3  0 0 0 0 0 ] $Liquid_Density;

sigma sigma [ 1 0 -2 0 0 0 0 ] $Surface_tension;



// ************************************************************************* //
    ''')
    liquid_nu = parsed['Liquid_Viscosity']/parsed['Liquid_Density']
    gas_nu = parsed['Gas_Viscosity'] / parsed['Gas_Density']
    builded = transportProperties.substitute(Liquid_Viscosity=parsed['Liquid_Viscosity'], Liquid_Density=parsed['Liquid_Density'], Gas_Viscosity=parsed['Gas_Viscosity'], Gas_Density=parsed['Gas_Density'], Liquid_nu=liquid_nu, Gas_nu=gas_nu, Surface_tension=parsed['Surface_tension'])
    return builded


def physicalParameters_save(parsed):
    physicalParameters = Template(r'''
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | foam-extend: Open Source CFD                    |
|  \\    /   O peration     | Version:     4.0                                |
|   \\  /    A nd           | Web:         http://www.foam-extend.org         |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      physicalParameters;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// nozzleType
nozzleType "$Type";

h0 h0 [ 0 1 0 0 0 0 0] 1e-10;

hTol hTol [ 0 1 0 0 0 0 0] 1e-5;


Omega ($OmegaX $OmegaY $OmegaZ);

Oxyz     (0 0 0);

//Nozzle initial location
Jxyz0	($LocationX $LocationY $LocationZ);

//nozzle velocity magnitude, i.e. the magnitude of velocity at which nozzle moves, do not confuse it with jet velocity
NozzleVelocity NozzleVelocity [ 0 1 -1 0 0 0 0]	$Nozzle_velocity;

// unit tangential vector of nozzle motion path
NozzleMotionDir		($Motion_directionX $Motion_directionY $Motion_directionZ);

// unit tangential vector of jet direction

jetDir ($jet_directionX $jet_directionY $jet_directionZ)

JetR JetR  [0 1 0 0 0 0 0]	$Radius;

JetH JetH  [0 1 0 0 0 0 0]	$Height;

JetW JetW  [0 1 0 0 0 0 0]	$Width;

JetL JetL  [0 1 0 0 0 0 0]	$Length;

JetAngle JetAngle  [0 0 0 0 0 0 0]	$Angle; //45 degree


hFixedVal hFixedVal  [0 1 0 0 0 0 0]	$Fixed_thickness;

UMagFixedVal UMagFixedVal  [0 1 -1 0 0 0 0]	$Jet_velocity;


// ************************************************************************* //
    ''')
    parsed['OmegaX'] = parsed['OmegaX'] * (2 * 3.141592) / 60
    parsed['OmegaY'] = parsed['OmegaY'] * (2 * 3.141592) / 60
    parsed['OmegaZ'] = parsed['OmegaZ'] * (2 * 3.141592) / 60
    UnitX = parsed['Motion_directionX'] / (parsed['Motion_directionX']**2 + parsed['Motion_directionY']**2 + parsed['Motion_directionZ']**2) ** (1/2)
    UnitY = parsed['Motion_directionY'] / (parsed['Motion_directionX']**2 + parsed['Motion_directionY']**2 + parsed['Motion_directionZ']**2) ** (1/2)
    UnitZ = parsed['Motion_directionZ'] / (parsed['Motion_directionX']**2 + parsed['Motion_directionY']**2 + parsed['Motion_directionZ']**2) ** (1/2)
    UnitXX = parsed['jet_directionX'] / (parsed['jet_directionX']**2 + parsed['jet_directionY']**2 + parsed['jet_directionZ']**2) ** (1/2)
    UnitYY = parsed['jet_directionY'] / (parsed['jet_directionX']**2 + parsed['jet_directionY']**2 + parsed['jet_directionZ']**2) ** (1/2)
    UnitZZ = parsed['jet_directionZ'] / (parsed['jet_directionX']**2 + parsed['jet_directionY']**2 + parsed['jet_directionZ']**2) ** (1/2)
    parsed['Motion_directionX'] = UnitX
    parsed['Motion_directionY'] = UnitY
    parsed['Motion_directionZ'] = UnitZ
    parsed['jet_directionX'] = UnitXX
    parsed['jet_directionY'] = UnitYY
    parsed['jet_directionZ'] = UnitZZ
    parsed['Angle'] = parsed['Angle'] * 3.141592 / 180
    builded = physicalParameters.substitute(Type=parsed['Type'], OmegaX=parsed['OmegaX'], OmegaY=parsed['OmegaY'], OmegaZ=parsed['OmegaZ'], LocationX=parsed['LocationX'], LocationY=parsed['LocationY'], LocationZ=parsed['LocationZ'], Nozzle_velocity=parsed['Nozzle_velocity'], Motion_directionX=parsed['Motion_directionX'], Motion_directionY=parsed['Motion_directionY'], Motion_directionZ=parsed['Motion_directionZ'], Radius=parsed['Radius'], Height=parsed['Height'], Width=parsed['Width'], Angle=parsed['Angle'], Length=parsed['Length'], Fixed_thickness=parsed['Fixed_thickness'], Jet_velocity=parsed['Jet_velocity'], jet_directionX=parsed['jet_directionX'], jet_directionY=parsed['jet_directionY'], jet_directionZ=parsed['jet_directionZ'])
    return builded

def g_save(parsed):
    g = Template(r'''
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | foam-extend: Open Source CFD                    |
|  \\    /   O peration     | Version:     4.0                                |
|   \\  /    A nd           | Web:         http://www.foam-extend.org         |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class         uniformDimensionedVectorField;
    location    "constant";
    object       g;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 -2 0 0 0 0];
value           ($GravityX $GravityY $GravityZ);


// ************************************************************************* //
    ''')
    builded = g.substitute(GravityX=parsed['GravityX'], GravityY=parsed['GravityY'], GravityZ=parsed['GravityZ'])
    return builded


def controlDict_save(parsed):
    controlDict = Template(r'''
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | foam-extend: Open Source CFD                    |
|  \\    /   O peration     | Version:     4.0                                |
|   \\  /    A nd           | Web:         http://www.foam-extend.org         |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

libs
(
    "liblduSolvers.so"
)

application     samsungFoamFV;

startFrom       startTime;

startTime       $Start_time;

stopAt          endTime;

endTime         $End_time;

deltaT          $Time_step;

writeControl    timeStep;

writeInterval   $Write_interval;

purgeWrite      0;

writeFormat     ascii;

writePrecision  6;

writeCompression uncompressed;

timeFormat      general;

timePrecision   6;

runTimeModifiable yes;

adjustTimeStep      no;

maxCo               2;

maxDeltaT           0.1;


// ************************************************************************* //
    ''')
    builded = controlDict.substitute(Start_time=parsed['Start_time'], End_time=parsed['End_time'], Time_step=parsed['Time_step'], Write_interval=parsed['Write_interval'])
    return builded

def fvSchemes_save(parsed):
    fvSchemes = Template(r'''
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | foam-extend: Open Source CFD                    |
|  \\    /   O peration     | Version:     4.0                                |
|   \\  /    A nd           | Web:         http://www.foam-extend.org         |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSchemes;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

ddtSchemes
{
    default         none;
    ddt(h,U) Euler;
    ddt(h) Euler;
    ddt(psi) Euler;
}

gradSchemes
{
    default Gauss linear;
    grad(psi) Gauss linear;
}

divSchemes
{
    default        Gauss linear;
    div(phi,h)     Gauss Gamma 0.5;
    div(phi2,U)    Gauss upwind;
    div(phiC,U)    Gauss upwind;
    div(phiC,UB)   Gauss upwind;
    div(phi,alpha)  Gauss vanLeer01;
    div(phirb,alpha) Gauss linear;
    div(phiIntrfc,psi)	Gauss upwind;
}

laplacianSchemes
{
    default none;
    laplacian(h) Gauss linear corrected;
    laplacian(Gamma,U) Gauss linear corrected;
}

interpolationSchemes
{
    default    linear;
}

snGradSchemes
{
    default    corrected;
}


// ************************************************************************* //
    ''')

def fvSolution_save(parsed):
    fvSolution = Template(r'''
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | foam-extend: Open Source CFD                    |
|  \\    /   O peration     | Version:     4.0                                |
|   \\  /    A nd           | Web:         http://www.foam-extend.org         |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSolution;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

solvers
{
    psi
    {
        solver          BiCGStab;
        preconditioner  ILU0;
        tolerance       $psi_abs;
        relTol          $psi_rel;
    }

    U
    {
        solver          BiCGStab;
        preconditioner  ILU0;
        tolerance       $u_abs;
        relTol          $u_rel;
    }

    h
    {
        solver          BiCGStab;
        preconditioner  ILU0;
        tolerance       $h_abs;
        relTol          $h_rel;
    }
}

nOuter 15;

fCo   0;  //0.0125;

LapSwitch 0.;


PISO
{
    cAlpha          1;
}

PIMPLE
{
    momentumPredictor yes;
    nOuterCorrectors $Iterations;
    nCorrectors     4;
    nNonOrthogonalCorrectors 0;
    nAlphaCorr      2;
    nAlphaSubCycles 2;
}

relaxationFactors
{
    h $h_relax;
    U $u_relax;
}
// ************************************************************************* //
    ''')

    builded = fvSolution.substitute(Iterations=parsed['Iterations'], psi_abs=parsed['psi_abs'], psi_rel=parsed['psi_rel'], u_abs=parsed['u_abs'], u_rel=parsed['u_rel'], h_abs=parsed['h_abs'], h_rel=parsed['h_rel'], u_relax=parsed['u_relax'], h_relax=parsed['h_relax'])

    return builded

