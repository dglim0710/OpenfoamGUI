from string import Template
import globalvar


def mesh_save():
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
    builded = mesh_script.substitute(Mesh_size=globalvar.VariableDict['Mesh_size'],
                                     Case_folder_path=globalvar.Case_folder_path)
    return builded

def transportProperties_save_no_2p():
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

//mug mug [0 2 -1 0 0 0 0] 0;
//mul mul [0 2 -1 0 0 0 0] 1e-3;
mug mug [1 -1 -1 0 0 0 0] $Gas_Viscosity;
mul mul [1 -1 -1 0 0 0 0] $Liquid_Viscosity;

rhog rhog [ 1 -3  0 0 0 0 0 ] $Gas_Density;
rhol rhol [ 1 -3  0 0 0 0 0 ] $Liquid_Density;

sigma sigma [ 1 0 -2 0 0 0 0 ] $Surface_tension;

h0 h0 [ 0 1 0 0 0 0 0] 1e-10;

Omega ($OmegaX $OmegaY $OmegaZ);
Oxyz     (0 0 0);

fCo   0;  //0.0125;

LapSwitch 0.;

//Nozzle initial location
Jxyz0	($LocationX $LocationY $LocationZ);

//nozzle velocity magnitude, i.e. the magnitude of velocity at which nozzle moves, do not confuse it with jet velocity
NozzleVel	$Nozzle_velocity;

// nozzleType
nozzleType "$Type";

// unit tangential vector of nozzle motion path
NozzleMotionDir		($Motion_directionX $Motion_directionY $Motion_directionZ);
jetDir ($jet_directionX $jet_directionY $jet_directionZ);

JetR	$Radius;

JetH	$Height;
JetW	$Width;
JetL	$Length;
JetAngle	$Angle; //45 degree

hFixedVal	$Fixed_thickness;
UMagFixedVal	$Jet_velocity;

// ************************************************************************* //
    ''')
    OmegaX_rad = globalvar.VariableDict['OmegaX'] * (2. * 3.141592) / 60.
    OmegaY_rad = globalvar.VariableDict['OmegaY'] * (2. * 3.141592) / 60.
    OmegaZ_rad = globalvar.VariableDict['OmegaZ'] * (2. * 3.141592) / 60.
    UnitX = globalvar.VariableDict['Motion_directionX'] / (globalvar.VariableDict['Motion_directionX']**2 + globalvar.VariableDict['Motion_directionY']**2 + globalvar.VariableDict['Motion_directionZ']**2) ** (1/2)
    UnitY = globalvar.VariableDict['Motion_directionY'] / (globalvar.VariableDict['Motion_directionX']**2 + globalvar.VariableDict['Motion_directionY']**2 + globalvar.VariableDict['Motion_directionZ']**2) ** (1/2)
    UnitZ = globalvar.VariableDict['Motion_directionZ'] / (globalvar.VariableDict['Motion_directionX']**2 + globalvar.VariableDict['Motion_directionY']**2 + globalvar.VariableDict['Motion_directionZ']**2) ** (1/2)
    UnitXX = globalvar.VariableDict['jet_directionX'] / (globalvar.VariableDict['jet_directionX']**2 + globalvar.VariableDict['jet_directionY']**2 + globalvar.VariableDict['jet_directionZ']**2) ** (1/2)
    UnitYY = globalvar.VariableDict['jet_directionY'] / (globalvar.VariableDict['jet_directionX']**2 + globalvar.VariableDict['jet_directionY']**2 + globalvar.VariableDict['jet_directionZ']**2) ** (1/2)
    UnitZZ = globalvar.VariableDict['jet_directionZ'] / (globalvar.VariableDict['jet_directionX']**2 + globalvar.VariableDict['jet_directionY']**2 + globalvar.VariableDict['jet_directionZ']**2) ** (1/2)
    Angle_rad = globalvar.VariableDict['Angle'] * 3.141592 / 180.
    if globalvar.Nozzle_shape == 'circular':
        nozzle_area = 3.141592 * (globalvar.VariableDict['Radius'])**2
    elif globalvar.Nozzle_shape == 'rectangular':
        nozzle_area = globalvar.VariableDict['Width'] * globalvar.VariableDict['Length']
    Flow_rate_velocity = globalvar.VariableDict['Jet_velocity'] * 0.001 / (60. * nozzle_area)
    builded = transportProperties.substitute(Liquid_Viscosity=globalvar.VariableDict['Liquid_Viscosity'],
                                             Liquid_Density=globalvar.VariableDict['Liquid_Density'],
                                             Gas_Viscosity=globalvar.VariableDict['Gas_Viscosity'],
                                             Gas_Density=globalvar.VariableDict['Gas_Density'],
                                             Surface_tension=globalvar.VariableDict['Surface_tension'],
                                             Type=globalvar.Nozzle_shape,
                                             OmegaX=OmegaX_rad,
                                             OmegaY=OmegaY_rad,
                                             OmegaZ=OmegaZ_rad,
                                             LocationX=globalvar.VariableDict['LocationX'],
                                             LocationY=globalvar.VariableDict['LocationY'],
                                             LocationZ=globalvar.VariableDict['LocationZ'],
                                             Nozzle_velocity=globalvar.VariableDict['Nozzle_velocity'],
                                             Motion_directionX=UnitX,
                                             Motion_directionY=UnitY,
                                             Motion_directionZ=UnitZ,
                                             Radius=globalvar.VariableDict['Radius'],
                                             Height=globalvar.VariableDict['Height'],
                                             Width=globalvar.VariableDict['Width'],
                                             Angle=Angle_rad,
                                             Length=globalvar.VariableDict['Length'],
                                             Fixed_thickness=globalvar.VariableDict['Fixed_thickness'],
                                             Jet_velocity=Flow_rate_velocity,
                                             jet_directionX=UnitXX,
                                             jet_directionY=UnitYY,
                                             jet_directionZ=UnitZZ)

    return builded


def transportProperties_save_2p():
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
    liquid_nu = globalvar.VariableDict['Liquid_Viscosity']/globalvar.VariableDict['Liquid_Density']
    gas_nu = globalvar.VariableDict['Gas_Viscosity'] / globalvar.VariableDict['Gas_Density']
    builded = transportProperties.substitute(Liquid_Viscosity=globalvar.VariableDict['Liquid_Viscosity'],
                                             Liquid_Density=globalvar.VariableDict['Liquid_Density'],
                                             Gas_Viscosity=globalvar.VariableDict['Gas_Viscosity'],
                                             Gas_Density=globalvar.VariableDict['Gas_Density'],
                                             Liquid_nu=liquid_nu,
                                             Gas_nu=gas_nu,
                                             Surface_tension=globalvar.VariableDict['Surface_tension'])
    return builded


def physicalParameters_save_2p():
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
    OmegaX_rad = globalvar.VariableDict['OmegaX'] * (2. * 3.141592) / 60.
    OmegaY_rad = globalvar.VariableDict['OmegaY'] * (2. * 3.141592) / 60.
    OmegaZ_rad = globalvar.VariableDict['OmegaZ'] * (2. * 3.141592) / 60.
    UnitX = globalvar.VariableDict['Motion_directionX'] / (globalvar.VariableDict['Motion_directionX']**2 + globalvar.VariableDict['Motion_directionY']**2 + globalvar.VariableDict['Motion_directionZ']**2) ** (1/2)
    UnitY = globalvar.VariableDict['Motion_directionY'] / (globalvar.VariableDict['Motion_directionX']**2 + globalvar.VariableDict['Motion_directionY']**2 + globalvar.VariableDict['Motion_directionZ']**2) ** (1/2)
    UnitZ = globalvar.VariableDict['Motion_directionZ'] / (globalvar.VariableDict['Motion_directionX']**2 + globalvar.VariableDict['Motion_directionY']**2 + globalvar.VariableDict['Motion_directionZ']**2) ** (1/2)
    UnitXX = globalvar.VariableDict['jet_directionX'] / (globalvar.VariableDict['jet_directionX']**2 + globalvar.VariableDict['jet_directionY']**2 + globalvar.VariableDict['jet_directionZ']**2) ** (1/2)
    UnitYY = globalvar.VariableDict['jet_directionY'] / (globalvar.VariableDict['jet_directionX']**2 + globalvar.VariableDict['jet_directionY']**2 + globalvar.VariableDict['jet_directionZ']**2) ** (1/2)
    UnitZZ = globalvar.VariableDict['jet_directionZ'] / (globalvar.VariableDict['jet_directionX']**2 + globalvar.VariableDict['jet_directionY']**2 + globalvar.VariableDict['jet_directionZ']**2) ** (1/2)
    Angle_rad = globalvar.VariableDict['Angle'] * 3.141592 / 180.
    if globalvar.Nozzle_shape == 'circular':
        nozzle_area = 3.141592 * (globalvar.VariableDict['Radius'])**2
    elif globalvar.Nozzle_shape == 'rectangular':
        nozzle_area = globalvar.VariableDict['Width'] * globalvar.VariableDict['Length']
    Flow_rate_velocity = globalvar.VariableDict['Jet_velocity'] * 0.001 / (60. * nozzle_area)
    builded = physicalParameters.substitute(Type=globalvar.Nozzle_shape,
                                            OmegaX=OmegaX_rad,
                                            OmegaY=OmegaY_rad,
                                            OmegaZ=OmegaZ_rad,
                                            LocationX=globalvar.VariableDict['LocationX'],
                                            LocationY=globalvar.VariableDict['LocationY'],
                                            LocationZ=globalvar.VariableDict['LocationZ'],
                                            Nozzle_velocity=globalvar.VariableDict['Nozzle_velocity'],
                                            Motion_directionX=UnitX,
                                            Motion_directionY=UnitY,
                                            Motion_directionZ=UnitZ,
                                            Radius=globalvar.VariableDict['Radius'],
                                            Height=globalvar.VariableDict['Height'],
                                            Width=globalvar.VariableDict['Width'],
                                            Angle=Angle_rad,
                                            Length=globalvar.VariableDict['Length'],
                                            Fixed_thickness=globalvar.VariableDict['Fixed_thickness'],
                                            Jet_velocity=Flow_rate_velocity,
                                            jet_directionX=UnitXX,
                                            jet_directionY=UnitYY,
                                            jet_directionZ=UnitZZ)
    return builded

def g_save():
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
    builded = g.substitute(GravityX=globalvar.VariableDict['GravityX'],
                           GravityY=globalvar.VariableDict['GravityY'],
                           GravityZ=globalvar.VariableDict['GravityZ'])
    return builded


def controlDict_save():
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
    builded = controlDict.substitute(Start_time=globalvar.VariableDict['Start_time'],
                                     End_time=globalvar.VariableDict['End_time'],
                                     Time_step=globalvar.VariableDict['Time_step'],
                                     Write_interval=globalvar.VariableDict['Write_interval'])
    return builded


def fvSchemes_save_2p():
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
    builded = fvSchemes.substitute()

    return builded

def fvSchemes_save_no_2p():
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
}

gradSchemes
{
    default Gauss linear;
}

divSchemes
{
    default        none;
    div(phi,h)     Gauss Gamma 0.5;
    div(phi2,U)    Gauss upwind;
    div(phiC,U)    Gauss upwind;
    div(phiC,UB)   Gauss upwind;
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
    builded = fvSchemes.substitute()

    return builded


def fvSolution_save_2p():
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

    builded = fvSolution.substitute(Iterations=globalvar.VariableDict['Iterations'],
                                    psi_abs=globalvar.VariableDict['psi_abs'],
                                    psi_rel=globalvar.VariableDict['psi_rel'],
                                    u_abs=globalvar.VariableDict['u_abs'],
                                    u_rel=globalvar.VariableDict['u_rel'],
                                    h_abs=globalvar.VariableDict['h_abs'],
                                    h_rel=globalvar.VariableDict['h_rel'],
                                    u_relax=globalvar.VariableDict['u_relax'],
                                    h_relax=globalvar.VariableDict['h_relax'])

    return builded


def fvSolution_save_no_2p():
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

nOuterCorrectors $Iterations;

relaxationFactors
{
    h $u_relax;
    U $h_relax;
}

// ************************************************************************* //
    ''')

    builded = fvSolution.substitute(Iterations=globalvar.VariableDict['Iterations'],
                                    u_abs=globalvar.VariableDict['u_abs'],
                                    u_rel=globalvar.VariableDict['u_rel'],
                                    h_abs=globalvar.VariableDict['h_abs'],
                                    h_rel=globalvar.VariableDict['h_rel'],
                                    u_relax=globalvar.VariableDict['u_relax'],
                                    h_relax=globalvar.VariableDict['h_relax'])

    return builded

def sampleDict_save():
    sampleDict = Template(r'''
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
    object      sampleSurfaceDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

interpolationScheme cellPoint;

surfaceFormat     raw;

writeFormat     raw;

setFormat raw;

fields
(
    h
    ih
);


sets
(
    thickness
    {
        type            uniform;
        axis            xyz;
        start           ($startX $startY $startZ);
        end             ($endX $endY $endZ);
        nPoints         $nPoints;
    }
);

surfaces
(

);


// ************************************************************************* //
    ''')

    builded = sampleDict.substitute(startX=globalvar.VariableDict['StartX'],
                                    startY=globalvar.VariableDict['StartY'],
                                    startZ=globalvar.VariableDict['StartZ'],
                                    endX=globalvar.VariableDict['EndX'],
                                    endY=globalvar.VariableDict['EndY'],
                                    endZ=globalvar.VariableDict['EndZ'],
                                    nPoints=globalvar.VariableDict['nPoints']
                                    )

    return builded
