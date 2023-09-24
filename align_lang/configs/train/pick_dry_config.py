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
    'bowl': ["brick", "metal", "cardboard", "tiles", "wooden", "granite", "cardboard", "plastic", "glass", "metal", "plastic", "polka dot", "checkerboard", "tiger", "magma", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow", "red and yellow stripe", "red and green stripe", "red and blue stripe", "red and purple stripe", "yellow and green stripe", "yellow and blue stripe", "yellow and purple stripe", "green and blue stripe", "green and purple stripe", "blue and purple stripe", "dark red and yellow stripe", "dark red and green stripe", "dark red and blue stripe", "dark red and purple stripe", "dark yellow and green stripe", "dark yellow and blue stripe", "dark yellow and purple stripe", "dark green and blue stripe", "dark green and purple stripe", "dark blue and purple stripe", "red and yellow polka dot", "red and green polka dot", "red and blue polka dot", "red and purple polka dot", "yellow and green polka dot", "yellow and blue polka dot", "yellow and purple polka dot", "green and blue polka dot", "green and purple polka dot", "blue and purple polka dot", "dark red and yellow polka dot", "dark red and green polka dot", "dark red and blue polka dot", "dark red and purple polka dot", "dark yellow and green polka dot", "dark yellow and blue polka dot", "dark yellow and purple polka dot", "dark green and blue polka dot", "dark green and purple polka dot", "dark blue and purple polka dot", "red swirl", "yellow swirl", "green swirl", "blue swirl", "purple swirl", "dark red swirl", "dark yellow swirl", "dark green swirl", "dark blue swirl", "dark purple swirl", "red paisley", "yellow paisley", "green paisley", "blue paisley", "purple paisley"],
}

ilga_phi_hat = {
    'bowl': ["brick", "metal", "cardboard", "tiles", "wooden", "granite", "cardboard", "plastic", "glass", "metal", "plastic", "polka dot", "checkerboard", "tiger", "magma", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow", "red and yellow stripe", "red and green stripe", "red and blue stripe", "red and purple stripe", "yellow and green stripe", "yellow and blue stripe", "yellow and purple stripe", "green and blue stripe", "green and purple stripe", "blue and purple stripe", "dark red and yellow stripe", "dark red and green stripe", "dark red and blue stripe", "dark red and purple stripe", "dark yellow and green stripe", "dark yellow and blue stripe", "dark yellow and purple stripe", "dark green and blue stripe", "dark green and purple stripe", "dark blue and purple stripe", "red and yellow polka dot", "red and green polka dot", "red and blue polka dot", "red and purple polka dot", "yellow and green polka dot", "yellow and blue polka dot", "yellow and purple polka dot", "green and blue polka dot", "green and purple polka dot", "blue and purple polka dot", "dark red and yellow polka dot", "dark red and green polka dot", "dark red and blue polka dot", "dark red and purple polka dot", "dark yellow and green polka dot", "dark yellow and blue polka dot", "dark yellow and purple polka dot", "dark green and blue polka dot", "dark green and purple polka dot", "dark blue and purple polka dot", "red swirl", "yellow swirl", "green swirl", "blue swirl", "purple swirl", "dark red swirl", "dark yellow swirl", "dark green swirl", "dark blue swirl", "dark purple swirl", "red paisley", "yellow paisley", "green paisley", "blue paisley", "purple paisley"],
    'drying rack': ["brick", "metal", "cardboard", "tiles", "wooden", "granite", "cardboard", "plastic", "glass", "metal", "plastic", "polka dot", "checkerboard", "tiger", "magma", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow", "red and yellow stripe", "red and green stripe", "red and blue stripe", "red and purple stripe", "yellow and green stripe", "yellow and blue stripe", "yellow and purple stripe", "green and blue stripe", "green and purple stripe", "blue and purple stripe", "dark red and yellow stripe", "dark red and green stripe", "dark red and blue stripe", "dark red and purple stripe", "dark yellow and green stripe", "dark yellow and blue stripe", "dark yellow and purple stripe", "dark green and blue stripe", "dark green and purple stripe", "dark blue and purple stripe", "red and yellow polka dot", "red and green polka dot", "red and blue polka dot", "red and purple polka dot", "yellow and green polka dot", "yellow and blue polka dot", "yellow and purple polka dot", "green and blue polka dot", "green and purple polka dot", "blue and purple polka dot", "dark red and yellow polka dot", "dark red and green polka dot", "dark red and blue polka dot", "dark red and purple polka dot", "dark yellow and green polka dot", "dark yellow and blue polka dot", "dark yellow and purple polka dot", "dark green and blue polka dot", "dark green and purple polka dot", "dark blue and purple polka dot", "red swirl", "yellow swirl", "green swirl", "blue swirl", "purple swirl", "dark red swirl", "dark yellow swirl", "dark green swirl", "dark blue swirl", "dark purple swirl", "red paisley", "yellow paisley", "green paisley", "blue paisley", "purple paisley"],
    'drying towel': ["brick", "metal", "cardboard", "tiles", "wooden", "granite", "cardboard", "plastic", "glass", "metal", "plastic", "polka dot", "checkerboard", "tiger", "magma", "rainbow", "blue", "cyan", "green", "olive", "orange", "pink", "purple", "red", "yellow", "dark blue", "dark cyan", "dark green", "dark orange", "dark pink", "dark purple", "dark red", "dark yellow", "red and yellow stripe", "red and green stripe", "red and blue stripe", "red and purple stripe", "yellow and green stripe", "yellow and blue stripe", "yellow and purple stripe", "green and blue stripe", "green and purple stripe", "blue and purple stripe", "dark red and yellow stripe", "dark red and green stripe", "dark red and blue stripe", "dark red and purple stripe", "dark yellow and green stripe", "dark yellow and blue stripe", "dark yellow and purple stripe", "dark green and blue stripe", "dark green and purple stripe", "dark blue and purple stripe", "red and yellow polka dot", "red and green polka dot", "red and blue polka dot", "red and purple polka dot", "yellow and green polka dot", "yellow and blue polka dot", "yellow and purple polka dot", "green and blue polka dot", "green and purple polka dot", "blue and purple polka dot", "dark red and yellow polka dot", "dark red and green polka dot", "dark red and blue polka dot", "dark red and purple polka dot", "dark yellow and green polka dot", "dark yellow and blue polka dot", "dark yellow and purple polka dot", "dark green and blue polka dot", "dark green and purple polka dot", "dark blue and purple polka dot", "red swirl", "yellow swirl", "green swirl", "blue swirl", "purple swirl", "dark red swirl", "dark yellow swirl", "dark green swirl", "dark blue swirl", "dark purple swirl", "red paisley", "yellow paisley", "green paisley", "blue paisley", "purple paisley"],
}

# ILGA PARAMS
epsilon = 0.5

# OPTIONAL
record_gui = False
display_debug_window = False
hide_arm_rgb = False