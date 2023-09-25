# TASK NAME
task_name = 'sweep_without_touching'
lang = 'sweep the dust into the bin'

# TASK CONFIG
# sweep the floor (ignore wooden floor)
task_kwargs = {
    'constraint': False,
    'dragged_obj_loc': [2],
    'possible_base_obj': ['sink'],
    'possible_base_obj_texture': ['blue'],
    'possible_dragged_obj': ['food'],
    'possible_dragged_obj_texture': ['green'],
    'possible_constraint_obj': ['floor'],
    'possible_constraint_obj_texture': ['wooden']
}

# sweep the floor (avoid rugs)
# task_kwargs = {
#     'constraint': True,
#     'dragged_obj_loc': [2],
#     'possible_base_obj': ['sink'],
#     'possible_base_obj_texture': ['blue'],
#     'possible_dragged_obj': ['food'],
#     'possible_dragged_obj_texture': ['green'],
#     'possible_constraint_obj': ['floor'],
#     'possible_constraint_obj_texture': ['carpet']
# }

max_steps = 3

# TASK-RELEVANT FEATURES
lga_phi_hat = {
    'dust': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'bin': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

ilga_phi_hat = {
    'dust': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'bin': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'floor': ["wooden", "granite", "styrofoam"],
}

# ILGA PARAMS
epsilon = 0.5

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False