# TASK NAME
task_name = 'visual_manipulation'
lang_goal = 'throw the food away'

# TASK CONFIG
# put down to closer object (both compost)
task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 1,
    'dragged_obj_loc': [2],
    'base_obj_loc': [4],
    'third_obj_loc' : [3],
    'fourth_obj_loc' : [2],
    'possible_dragged_obj': ['tomato'],
    'possible_dragged_obj_texture': ['red'],
    'possible_base_obj': ['box'],
    'possible_base_obj_texture': ['green'],
    'possible_third_obj': ['box'],
    'possible_third_obj_texture': ['green'],
    'possible_fourth_obj': ['bowl'],
    'possible_fourth_obj_texture': ['blue']
}

# pick up farther fruit (closer one is green)
task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 1,
    'dragged_obj_loc': [2],
    'base_obj_loc': [3],
    'third_obj_loc' : [4],
    'fourth_obj_loc' : [2],
    'possible_dragged_obj': ['tomato'],
    'possible_dragged_obj_texture': ['red'],
    'possible_base_obj': ['box'],
    'possible_base_obj_texture': ['green'],
    'possible_third_obj': ['box'],
    'possible_third_obj_texture': ['blue'],
    'possible_fourth_obj': ['bowl'],
    'possible_fourth_obj_texture': ['blue']
}

max_steps = 1

# TASK-RELEVANT FEATURES
lga_phi_hat = {
    'tomato': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'peach': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'pepper': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'apple': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

ilga_phi_hat = {
    'tomato': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'peach': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'pepper': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'apple': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'bin': ["green"],
    'box': ["green"],
}

gt_phi_hat = {
    'tomato': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'peach': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'pepper': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'apple': ["orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'bin': ["green", "dark green"],
    'box': ["green", "dark green"],
    'container': ["green", "dark green"],
}

# ILGA PARAMS
epsilon = 1

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False