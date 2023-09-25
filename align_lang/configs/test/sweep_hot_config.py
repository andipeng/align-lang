# TASK NAME
task_name = 'sweep_without_touching'
lang = 'sweep the food into the sink'

# TASK CONFIG
# sweep food into the sink (cold stove)
task_kwargs = {
    'constraint': False,
    'dragged_obj_loc': [2],
    'possible_base_obj': ['sink'],
    'possible_base_obj_texture': ['blue'],
    'possible_dragged_obj': ['food'],
    'possible_dragged_obj_texture': ['green'],
    'possible_constraint_obj': ['stove'],
    'possible_constraint_obj_texture': ['gray']
}

# sweep food into the sink (avoid hot stove)
# task_kwargs = {
#     'constraint': True,
#     'dragged_obj_loc': [2],
#     'possible_base_obj': ['sink'],
#     'possible_base_obj_texture': ['blue'],
#     'possible_dragged_obj': ['food'],
#     'possible_dragged_obj_texture': ['green'],
#     'possible_constraint_obj': ['stove'],
#     'possible_constraint_obj_texture': ['red']
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
    'stove': ["red", "dark red", "orange"],
    'knife': ["red", "dark red", "orange"],
    'container': ["red", "dark red", "orange"],
}

# ILGA PARAMS
epsilon = 0.5

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False