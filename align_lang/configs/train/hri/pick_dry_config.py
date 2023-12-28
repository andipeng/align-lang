# TASK NAME
task_name = 'visual_manipulation'
lang_goal = 'bring me a cereal bowl'

# TASK CONFIG
# pick up any bowl (closer, no rack)
task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 1,
    'dragged_obj_loc': [2],
    'base_obj_loc': [4],
    'third_obj_loc' : [1],
    'fourth_obj_loc' : [2],
    'possible_dragged_obj': ['bowl'],
    'possible_dragged_obj_texture': ['blue'],
    'possible_base_obj': ['square'],
    'possible_base_obj_texture': ['red'],
    'possible_third_obj': ['drying rack'],
    'possible_third_obj_texture': ['wooden'],
    'possible_fourth_obj': ['bowl'],
    'possible_fourth_obj_texture': ['blue']
}

# pick up dry bowl (farther, not on rack)
# task_kwargs = { 
#     'num_dragged_obj': 1,
#     'num_base_obj': 1,
#     'num_other_obj': 2,
#     'dragged_obj_loc': [1],
#     'base_obj_loc': [4],
#     'third_obj_loc' : [2],
#     'fourth_obj_loc' : [2],
#     'possible_dragged_obj': ['bowl'],
#     'possible_dragged_obj_texture': ['blue'],
#     'possible_base_obj': ['square'],
#     'possible_base_obj_texture': ['red'],
#     'possible_third_obj': ['drying rack'],
#     'possible_third_obj_texture': ['wooden'],
#     'possible_fourth_obj': ['bowl'],
#     'possible_fourth_obj_texture': ['blue']
# }

max_steps = 1

# TASK-RELEVANT FEATURES
lga_phi_hat = {
    'bowl': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

ilga_phi_hat = {
    'bowl': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'drying rack': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'drying towel': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'drying cloth': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

gt_phi_hat = {
    'bowl': ["brick","tiles","wooden", "granite", "glass", "styrofoam", "metal", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'drying rack': ["brick","tiles","wooden", "granite", "glass", "styrofoam", "metal", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'drying towel': ["brick","tiles","wooden", "granite", "glass", "styrofoam", "metal", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'drying cloth': ["brick","tiles","wooden", "granite", "glass", "styrofoam", "metal", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

# ILGA PARAMS
epsilon = 1

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False