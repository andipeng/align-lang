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
from align_lang.configs.train import pick_config, place_config, rotate_config, sweep_config

import vima_bench
from sentence_transformers import SentenceTransformer

parser = argparse.ArgumentParser()
parser.add_argument('--save_dir', type=str, default='expert_data')
parser.add_argument('--task', type=str, default='pick')
parser.add_argument('--mask', type=bool, default=False)
parser.add_argument('--num_trajs', type=int, default=10)
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--dart', type=bool, default=False)
parser.add_argument('--dart_mu', type=float, default=0.0)
parser.add_argument('--dart_std', type=float, default=0.05)
parser.add_argument('--dart_samples', type=int, default=5)
args = parser.parse_args()

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

################################### TASK SETUP #################################

if args.task == 'pick':
    config = pick_config
elif args.task == 'place':
    config = place_config
elif args.task == 'rotate':
    config = rotate_config
elif args.mask == 'sweep':
    config = sweep_config

env = vima_bench.make(task_name=config.task_name,task_kwargs=config.task_kwargs,record_gui=config.record_gui,hide_arm_rgb=config.hide_arm_rgb)

lang_model = SentenceTransformer('all-MiniLM-L6-v2', device=args.device)
lang_embed = lang_model.encode(config.lang_goal)

########################################################################

# generates random trajs within specified constraints
def gen_trajs(env, num_trajs, task_name, task_kwargs, goal, phi_hat):
    trajs = []
    task = env.task
    oracle_fn = task.oracle(env)
    for traj in tqdm(range(num_trajs)):
        traj = {'obs': [], 'mask_obs': [], 'obs_text': [], 'acts': [], 'goals':[], 'lang_goal': [], 'meta': []}
        obs = env.reset()
        traj['meta'] = env.meta_info
        traj['lang_goal'] = config.lang_goal
        obj_type = env.meta_info['obj_id_to_info'][6]['obj_name']

        # extracts ground truth text of scene objects
        for obj in env.meta_info['obj_id_to_info']:
            obj_name = env.meta_info['obj_id_to_info'][obj]['obj_name']
            obj_texture = env.meta_info['obj_id_to_info'][obj]['texture_name']
            traj['obs_text'].append([obj_name, obj_texture])

        #goal_embed = lang_model.encode(obj_type)
        for step in range(config.max_steps):
            mask_obs = obs['segm']['top'] # extracts segm
            top_obs = obs['rgb']['top'] # extracts top down view only
            traj['obs'].append(process_obs(top_obs))
            traj['mask_obs'].append(process_segm(mask_obs, phi_hat, env.meta_info['obj_id_to_info']))
            traj['goals'].append(lang_embed)
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
        traj['obs_text'] = np.array(traj['obs_text'])
        traj['acts'] = np.array(traj['acts'])
        traj['lang_goal'] = np.array(traj['lang_goal'])
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

trajs = gen_trajs(env=env, num_trajs=args.num_trajs, task_name=config.task_name, task_kwargs=config.task_kwargs, goal=lang_embed, phi_hat=config.phi_hat)
pickle.dump(trajs, open(args.save_dir + '/trajs.pkl', 'wb'))
env.close()