# TASK NAME
task_name = 'visual_manipulation'
lang_goal = 'bring me a fruit'

# TASK CONFIG
# pick up closer fruit (both ripe)
task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 1,
    'num_other_obj': 1,
    'dragged_obj_loc': [2],
    'base_obj_loc': [4],
    'third_obj_loc' : [1],
    'fourth_obj_loc' : [2],
    'possible_dragged_obj': ['tomato'],
    'possible_dragged_obj_texture': ['red'],
    'possible_base_obj': ['square'],
    'possible_base_obj_texture': ['blue'],
    'possible_third_obj': ['tomato'],
    'possible_third_obj_texture': ['red'],
    'possible_fourth_obj': ['tomato'],
    'possible_fourth_obj_texture': ['green']
}

# pick up farther fruit (closer one is green)
# task_kwargs = { 
#     'num_dragged_obj': 1,
#     'num_base_obj': 2,
#     'num_other_obj': 1,
#     'dragged_obj_loc': [1],
#     'base_obj_loc': [4],
#     'third_obj_loc' : [2],
#     'fourth_obj_loc' : [2],
#     'possible_dragged_obj': ['tomato'],
#     'possible_dragged_obj_texture': ['red'],
#     'possible_base_obj': ['square'],
#     'possible_base_obj_texture': ['blue'],
#     'possible_third_obj': ['tomato'],
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
    'peach': ["orange", "pink", "purple", "red", "yellow", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'tomato': ["orange", "pink", "purple", "red", "yellow", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'pepper': ["orange", "pink", "purple", "red", "yellow", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
    'apple': ["green", "orange", "pink", "purple", "red", "yellow", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow"],
}

# ILGA PARAMS
epsilon = 0.5

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False