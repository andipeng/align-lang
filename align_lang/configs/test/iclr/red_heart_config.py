# TASK NAME
task_name = 'visual_manipulation'
lang_goal = 'bring me a red heart'

# TASK CONFIG
task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 2,
    'dragged_obj_loc': [1,2],
    'base_obj_loc': [4],
    'third_obj_loc' : [2,3],
    'fourth_obj_loc' : [2,3],
    'possible_dragged_obj': ['heart'],
    'possible_dragged_obj_texture': ['red'],
    'possible_base_obj': ['pallet'],
    'possible_base_obj_texture': ['wooden'],
    'possible_third_obj': None,
    'possible_third_obj_texture': None,
    'possible_fourth_obj': None,
    'possible_fourth_obj_texture': None
}

max_steps = 1

# TASK-RELEVANT FEATURES
lga_phi_hat = {
    "heart": ["red","dark red","dark red swirl","red paisley"],
}

lga_hill_phi_hat = {
    "heart": ["red","dark red","dark red swirl","red paisley"],
}

human_phi_hat = {
    "heart": ["red","dark red","dark red swirl","red paisley"],
}

ilga_phi_hat = None

gt_phi_hat = {
    "heart": ["red","dark red","dark red swirl","red paisley"],
}

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False