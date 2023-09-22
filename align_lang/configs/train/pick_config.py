# TASK NAME
task_name = 'visual_manipulation'
lang_goal = 'bring me the red block'

# TASK CONFIG
task_kwargs = {
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 0,
    'dragged_obj_loc': [1,2],
    'base_obj_loc': [4],
    'third_obj_loc' : [1],
    'fourth_obj_loc' : [3],
    'possible_dragged_obj': ['block'],
    'possible_dragged_obj_texture': ['red'],
    'possible_base_obj': ['pan'],
    'possible_base_obj_texture': ['tiger'],
    'possible_third_obj': ['bowl'],
    'possible_third_obj_texture': ['blue'],
    'possible_fourth_obj': ['pentagon'],
    'possible_fourth_obj_texture': ['blue']
}

max_steps = 1

# TASK-RELEVANT FEATURES
phi_hat = {
    'block': ['red'],
}

# ILGA PARAMS
epsilon = 0.5

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False