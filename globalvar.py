from collections import OrderedDict

global n
global Case_folder_path
global Of_folder_path
global twophase_check
global Nozzle_shape

Nozzle_shape = 'rectangular'
# twophase_check = 1 >>>> 2 Phase
# twophase_check = 0 >>>> Do not use 2 phase
twophase_check = 0
n = 0
Case_folder_path = '! Set the path of a simulation folder !'
Of_folder_path = '! Set the path of the Openfoam folder !'
VariableDict = OrderedDict([
    ('Liquid_Density', 0.),
    ('Liquid_Viscosity', 0.),
    ('Gas_Density', 0.),
    ('Gas_Viscosity', 0.),
    ('Surface_tension', 0),
    ('GravityX', 0.),
    ('GravityY', 0.),
    ('GravityZ', -9.81),
    ####################################################################################################################
    ('Type', Nozzle_shape),
    ('LocationX', 0.),
    ('LocationY', 0.),
    ('LocationZ', 0.),
    ('OmegaX', 0.),
    ('OmegaY', 0.),
    ('OmegaZ', 0.),
    ('Motion_directionX', 1.),
    ('Motion_directionY', 0.),
    ('Motion_directionZ', 0.),
    ('jet_directionX', 1.),
    ('jet_directionY', 0.),
    ('jet_directionZ', 0.),
    ('Nozzle_velocity', 0.),
    ('Radius', 0.005),
    ('Width', 0.0004),
    ('Height', 0.0066),
    ('Length', 0.011),
    ('Angle', 45.),
    ('Fixed_thickness', 0.0005),
    ('Jet_velocity', 0.),
    ####################################################################################################################
    ('Start_time', 0.),
    ('End_time', 0.),
    ('Time_step', 1e-6),
    ('Write_interval', 100),
    ('psi_abs', 0.),
    ('psi_rel', 0.),
    ('u_abs', 0.),
    ('u_rel', 0.),
    ('h_abs', 0.),
    ('h_rel', 0.),
    ('u_relax', 0.),
    ('h_relax', 0.),
    ('Iterations', 0.),
    ####################################################################################################################
    ('Mesh_Type', 'Triangular'),
    ('Mesh_size', 0.0025),
    ('longseg', 825),
    ('shortseg', 10),
    ####################################################################################################################
    ('StartX', 0.),
    ('StartY', 0.),
    ('StartZ', 0.),
    ('EndX', 0.),
    ('EndY', 0.),
    ('EndZ', 0.),
    ('nPoints', 0.),
    ('Sampling_time', 0.)
])