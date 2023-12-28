# TASK NAME
task_name = 'visual_manipulation'
lang_goal = 'put down the pan'

# TASK CONFIG
# put down to closer object (both pallet)
task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 1,
    'dragged_obj_loc': [2],
    'base_obj_loc': [4],
    'third_obj_loc' : [3],
    'fourth_obj_loc' : [2],
    'possible_dragged_obj': ['pan'],
    'possible_dragged_obj_texture': ['metal'],
    'possible_base_obj': ['pallet'],
    'possible_base_obj_texture': ['granite'],
    'possible_third_obj': ['pallet'],
    'possible_third_obj_texture': ['granite'],
    'possible_fourth_obj': ['bowl'],
    'possible_fourth_obj_texture': ['blue']
}

# pick up farther fruit (closer one is green)
# task_kwargs = { 
#     'num_dragged_obj': 1,
#     'num_base_obj': 1,
#     'num_other_obj': 1,
#     'dragged_obj_loc': [2],
#     'base_obj_loc': [3],
#     'third_obj_loc' : [4],
#     'fourth_obj_loc' : [2],
#     'possible_dragged_obj': ['pan'],
#     'possible_dragged_obj_texture': ['metal'],
#     'possible_base_obj': ['pallet'],
#     'possible_base_obj_texture': ['granite'],
#     'possible_third_obj': ['coaster'],
#     'possible_third_obj_texture': ['granite'],
#     'possible_fourth_obj': ['bowl'],
#     'possible_fourth_obj_texture': ['blue']
# }

max_steps = 1

# TASK-RELEVANT FEATURES
lga_phi_hat = {
    'pan': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

ilga_phi_hat = {
    'pan': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'coaster': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

gt_phi_hat = {
    'pan': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'coaster': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'pallet': ["granite", "glass", "styrofoam", "metal", "wooden", "carpet", "tiles", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

# ILGA PARAMS
epsilon = 1

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False