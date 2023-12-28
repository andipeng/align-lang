# TASK NAME
task_name = 'visual_manipulation'
lang_goal = 'bring me my favorite food'

# TASK CONFIG
# pick up closer mug (both clean)
task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 1,
    'dragged_obj_loc': [2],
    'base_obj_loc': [4],
    'third_obj_loc' : [1],
    'fourth_obj_loc' : [2],
    'possible_dragged_obj': ['apple'],
    'possible_dragged_obj_texture': ['green'],
    'possible_base_obj': ['square'],
    'possible_base_obj_texture': ['red'],
    'possible_third_obj': ['pepper'],
    'possible_third_obj_texture': ['green'],
    'possible_fourth_obj': ['tomato'],
    'possible_fourth_obj_texture': ['green']
}

# pick up farther bowl (closer mug)
# task_kwargs = { 
#     'num_dragged_obj': 1,
#     'num_base_obj': 2,
#     'num_other_obj': 1,
#     'dragged_obj_loc': [1],
#     'base_obj_loc': [4],
#     'third_obj_loc' : [2],
#     'fourth_obj_loc' : [2],
#     'possible_dragged_obj': ['bowl'],
#     'possible_dragged_obj_texture': ['green'],
#     'possible_base_obj': ['square'],
#     'possible_base_obj_texture': ['red'],
#     'possible_third_obj': ['mug'],
#     'possible_third_obj_texture': ['green'],
#     'possible_fourth_obj': ['bowl'],
#     'possible_fourth_obj_texture': ['blue']
# }

max_steps = 1

# TASK-RELEVANT FEATURES
lga_phi_hat = {
    'peach': ["rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'tomato': ["rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'pepper': ["rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'apple': ["rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

ilga_phi_hat = {
    'peach': ["blue", "cyan", "green", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'apple': ["blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

gt_phi_hat = {
    'peach': ["rainbow","blue", "cyan", "green", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'apple': ["rainbow","blue", "cyan", "green", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'pepper': ["rainbow","blue", "cyan", "green", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

# ILGA PARAMS
epsilon = 1

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False