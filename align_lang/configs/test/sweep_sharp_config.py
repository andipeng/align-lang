# TASK NAME
task_name = 'sweep_without_touching'
lang = 'sweep the food into the sink'

# TASK CONFIG
# sweep food into the sink (ignore food in way)
task_kwargs = {
    'constraint': True,
    'dragged_obj_loc': [2],
    'possible_base_obj': ['sink'],
    'possible_base_obj_texture': ['blue'],
    'possible_dragged_obj': ['food'],
    'possible_dragged_obj_texture': ['green'],
    'possible_constraint_obj': ['food'],
    'possible_constraint_obj_texture': ['green']
}

# sweep food into the sink (avoid knife)
# task_kwargs = {
#     'constraint': True,
#     'dragged_obj_loc': [2],
#     'possible_base_obj': ['sink'],
#     'possible_base_obj_texture': ['blue'],
#     'possible_dragged_obj': ['food'],
#     'possible_dragged_obj_texture': ['green'],
#     'possible_constraint_obj': ['knife'],
#     'possible_constraint_obj_texture': ['green']
# }

max_steps = 3

# TASK-RELEVANT FEATURES
lga_phi_hat = {
    'food': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'sink': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

ilga_phi_hat = {
    'food': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'sink': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'knife': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'sharp block': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

# ILGA PARAMS
epsilon = 0.5

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False