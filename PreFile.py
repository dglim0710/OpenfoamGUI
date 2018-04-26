from string import Template


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
    parsed['Motion_directionX'] = UnitX
    parsed['Motion_directionY'] = UnitY
    parsed['Motion_directionZ'] = UnitZ
    parsed['Angle'] = parsed['Angle'] * 3.141592 / 180
    builded = physicalParameters.substitute(Type=parsed['Type'], OmegaX=parsed['OmegaX'], OmegaY=parsed['OmegaY'], OmegaZ=parsed['OmegaZ'], LocationX=parsed['LocationX'], LocationY=parsed['LocationY'], LocationZ=parsed['LocationZ'], Nozzle_velocity=parsed['Nozzle_velocity'], Motion_directionX=parsed['Motion_directionX'], Motion_directionY=parsed['Motion_directionY'], Motion_directionZ=parsed['Motion_directionZ'], Radius=parsed['Radius'], Height=parsed['Height'], Width=parsed['Width'], Angle=parsed['Angle'], Length=parsed['Length'], Fixed_thickness=parsed['Fixed_thickness'], Jet_velocity=parsed['Jet_velocity'])
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

