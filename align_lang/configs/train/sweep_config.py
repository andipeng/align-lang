# TASK NAME
task_name = 'sweep_without_touching'
lang = 'sweep the food into the sink'

# TASK CONFIG
task_kwargs = {
    'constraint': False,
    'dragged_obj_loc': [4],
    'possible_base_obj': ['three-sided rectangle'],
    'possible_base_obj_texture': ['blue'],
    'possible_dragged_obj': ['small block'],
    'possible_dragged_obj_texture': ['green'],
    'possible_constraint_obj': ['line'],
    'possible_constraint_obj_texture': ['red']
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