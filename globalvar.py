from collections import OrderedDict

global n
global Case_folder_path
global Of_folder_path
global twophase_check
global Nozzle_shape

Nozzle_shape = 'circular'
twophase_check = 1
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
    ('GravityZ', 0.),
    ####################################################################################################################
    ('Type', 0.),
    ('LocationX', 0.),
    ('LocationY', 0.),
    ('LocationZ', 0.),
    ('OmegaX', 0.),
    ('OmegaY', 0.),
    ('OmegaZ', 0.),
    ('Motion_directionX', 0.),
    ('Motion_directionY', 0.),
    ('Motion_directionZ', 0.),
    ('jet_directionX', 0.),
    ('jet_directionY', 0.),
    ('jet_directionZ', 0.),
    ('Nozzle_velocity', 0.),
    ('Radius', 0.),
    ('Width', 0.),
    ('Height', 0.),
    ('Length', 0.),
    ('Angle', 0.),
    ('Fixed_thickness', 0.),
    ('Jet_velocity', 0.),
    ####################################################################################################################
    ('Start_time', 0.),
    ('End_time', 0.),
    ('Time_step', 0.),
    ('Write_interval', 0.),
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
    ('Mesh_Type', 0.),
    ('Mesh_size', 0.)
])