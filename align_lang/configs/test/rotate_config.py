# TASK NAME
task_name = 'rotate'
lang_goal = 'rotate the red block'

# TASK CONFIG
task_kwargs = {
    'num_dragged_obj': 1,
    'num_distractors_obj': 0,
    'possible_angles_of_rotation': 120,
    'possible_dragged_obj': ['pan'],
    'possible_dragged_obj_texture': ['blue']
}

max_steps = 1

# TASK-RELEVANT FEATURES
phi_hat = {
    'block': ['red'],
}

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False