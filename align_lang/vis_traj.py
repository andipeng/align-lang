import os
import string
import re
import random
import pickle
import argparse
import numpy as np

import vima_bench
from align_lang.utils import process_obs, process_segm, reconstruct_act

parser = argparse.ArgumentParser()
parser.add_argument('--traj_file', type=str, default='expert_data/trajs.pkl')
parser.add_argument('--task_name', type=str, default='visual_manipulation')
args = parser.parse_args()

task_kwargs = { 
    'num_dragged_obj': 1,
    'num_base_obj': 2,
    'num_other_obj': 1,
    'dragged_obj_loc': [1],
    'base_obj_loc': [4],
    'third_obj_loc' : [2],
    'fourth_obj_loc' : [3],
    'possible_dragged_obj': ['tomato'],
    'possible_dragged_obj_texture': ['red'],
    'possible_base_obj': ['square'],
    'possible_base_obj_texture': ['blue'],
    'possible_third_obj': ['tomato'],
    'possible_third_obj_texture': ['green'],
    'possible_fourth_obj': ['star'],
    'possible_fourth_obj_texture': ['yellow']
}

########################################################################

trajs = pickle.load(open(args.traj_file,'rb'))

env = vima_bench.make(task_name=args.task_name,task_kwargs=task_kwargs,display_debug_window=True,hide_arm_rgb=False)
task = env.task
oracle_fn = task.oracle(env)

obs = env.reset()
for step in range(3):
    oracle_action = oracle_fn.act(obs)
    # clip action
    #oracle_action = {
    #    k: np.clip(v, env.action_space[k].low, env.action_space[k].high)
    #        for k, v in oracle_action.items()
    #    }
    #traj['acts'].append(flatten_act(oracle_action))
    action = trajs[0]['acts']

    print(action)
    obs, _, done, info = env.step(action=reconstruct_act(action,env), skip_oracle=False)

env.close()