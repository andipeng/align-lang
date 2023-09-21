import os
import string
import re
import random
import pickle
import argparse
from tqdm import tqdm
import numpy as np
import statistics

from align_lang.utils import process_obs, process_segm, flatten_act

import vima_bench
from sentence_transformers import SentenceTransformer

########################## PHI_HAT ####################################
phi_hat = {
    'block': ['red'],
}

########################## TASK DEF ####################################
visual_man_task_kwargs = {'num_dragged_obj': 1,
     'num_base_obj': 1,
     'num_other_obj': 0,
     'dragged_obj_loc': [1],
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
     'possible_fourth_obj_texture': ['blue']}
rotate_task_kwargs = {'num_dragged_obj': 1,
               'num_distractors_obj': 0,
               'possible_angles_of_rotation': 120,
               'possible_dragged_obj': ['pan'],
               'possible_dragged_obj_texture': ['blue']}
sweep_task_kwargs = {'num_dragged_obj': 1,
               'num_distractors_obj': 0,
               'possible_dragged_obj': ['pan'],
               'possible_dragged_obj_texture': ['blue']}
########################## TASK DEF ####################################

parser = argparse.ArgumentParser()
parser.add_argument('--save_dir', type=str, default='expert_data')
parser.add_argument('--task', type=str, default='visual_manipulation')
parser.add_argument('--mask', type=bool, default=False)
parser.add_argument('--num_trajs', type=int, default=10)
parser.add_argument('--max_steps', type=int, default=1)
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--dart', type=bool, default=True)
parser.add_argument('--dart_mu', type=int, default=0.0)
parser.add_argument('--dart_std', type=int, default=0.05)
parser.add_argument('--dart_samples', type=int, default=5)
args = parser.parse_args()

########################## LANG DEF ####################################

lang_model = SentenceTransformer('all-MiniLM-L6-v2', device=args.device)
lang_goal = 'bring me the bowl'
lang_embed = lang_model.encode(lang_goal)

########################################################################

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

#record_gui=True, display_debug_window=True, hide_arm_rgb=False
if args.task == 'visual_manipulation':
    task_kwargs = visual_man_task_kwargs
    env = vima_bench.make(task_name=args.task,task_kwargs=task_kwargs,hide_arm_rgb=False)
elif args.task == 'rotate':
    task_kwargs = rotate_task_kwargs
    env = vima_bench.make(task_name=args.task,task_kwargs=rotate_task_kwargs,hide_arm_rgb=False)
elif args.task == 'sweep_without_touching':
    task_kwargs = sweep_task_kwargs
    env = vima_bench.make(task_name=args.task,task_kwargs=sweep_task_kwargs,hide_arm_rgb=False)

# generates random trajs within specified constraints
def gen_trajs(env, num_trajs, task_name, task_kwargs, goal, phi_hat):
    trajs = []
    task = env.task
    oracle_fn = task.oracle(env)
    for traj in tqdm(range(num_trajs)):
        traj = {'obs': [], 'mask_obs': [], 'acts': [], 'goals':[], 'meta': []}
        obs = env.reset()
        traj['meta'] = env.meta_info
        obj_type = env.meta_info['obj_id_to_info'][6]['obj_name']
        goal_embed = lang_model.encode(obj_type)
        for step in range(args.max_steps):
            mask_obs = obs['segm']['top'] # extracts segm
            top_obs = obs['rgb']['top'] # extracts top down view only
            traj['obs'].append(process_obs(top_obs))
            traj['mask_obs'].append(process_segm(mask_obs, phi_hat, env.meta_info['obj_id_to_info']))
            traj['goals'].append(goal_embed)
            # prompt, prompt_assets = env.prompt, env.prompt_assets
            oracle_action = oracle_fn.act(obs)
            # clip action
            oracle_action = {
                k: np.clip(v, env.action_space[k].low, env.action_space[k].high)
                for k, v in oracle_action.items()
            }
            traj['acts'].append(flatten_act(oracle_action))
            obs, _, done, info = env.step(action=oracle_action, skip_oracle=False)
        traj['obs'] = np.array(traj['obs'])
        traj['mask_obs'] = np.array(traj['mask_obs'])
        traj['acts'] = np.array(traj['acts'])
        traj['goals'] = np.array(traj['goals'])
        traj['meta'] = np.array(traj['meta'])
        trajs.append(traj)

    if args.dart: # iterates through and adds Gaussian noise to trajectories
        for traj in trajs:
            for sample in range(args.dart_samples):
                noisy_traj = {'obs': [],'acts': [], 'goals':[], 'meta': []}
                noisy_traj['meta'] = env.meta_info
                
                # injects Gaussian noise
                for action in traj['acts']:
                    noise = np.random.normal(args.dart_mu, args.dart_std*np.std(action), action.shape)
                    action_noisy = action + noise
                    noisy_traj['acts'].append(action_noisy)
                for state in traj['obs']:
                    noise = np.random.normal(args.dart_mu, args.dart_std*np.std(state), state.shape)
                    state_noisy = state + noise
                    noisy_traj['obs'].append(state_noisy)
                trajs.append(noisy_traj)
    return trajs

trajs = gen_trajs(env=env, num_trajs=args.num_trajs, task_name=args.task, task_kwargs=task_kwargs, goal=lang_embed, phi_hat=phi_hat)
pickle.dump(trajs, open(args.save_dir + '/trajs.pkl', 'wb'))
env.close()