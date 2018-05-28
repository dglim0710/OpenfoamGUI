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
stepN = 1
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
    ('Radius', 0.005),
    ('Width', 0.0004),
    ('Height', 0.0066),
    ('Length', 0.011),
    ('Angle', 45.),
    ('Fixed_thickness', 0.0005),
    ####################################################################################################################
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
    ('Sampling_time', 0.),
    ('Initial_LocationX1', 0.), ('Initial_LocationY1', 0.), ('Initial_LocationZ1', 0.), ('Final_LocationX1', 0.),
    ('Final_LocationY1', 0.), ('Final_LocationZ1', 0.), ('jet_directionX1', 0.), ('jet_directionY1', 0.),
    ('jet_directionZ1', 0.), ('OmegaZ1', 0.), ('Process_time1', 0.), ('Fixed_thickness1', 0.), ('Jet_velocity1', 0.),
    ('Time_step1', 0.),  ('Write_interval1', 0.)
])