# TASK NAME
task_name = 'sweep_without_touching'
lang = 'sweep the food into the sink'

# TASK CONFIG
task_kwargs = {
    'num_dragged_obj': 1,
    'num_distractors_obj': 0,
    'possible_dragged_obj': ['pan'],
    'possible_dragged_obj_texture': ['red']
}

max_steps = 3

# TASK-RELEVANT FEATURES
phi_hat = {
    'pan': ['red'],
}

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False