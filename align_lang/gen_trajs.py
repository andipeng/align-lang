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
from align_lang.configs.train import pick_dry_config, pick_food_config, pick_ripe_config, place_content_config, place_electronic_config, place_stable_config, sweep_hot_config, sweep_rug_config, sweep_sharp_config

import vima_bench
from sentence_transformers import SentenceTransformer

parser = argparse.ArgumentParser()
parser.add_argument('--save_dir', type=str, default='expert_data')
parser.add_argument('--task', type=str, default='pick_dry')
parser.add_argument('--mask', type=bool, default=False)
parser.add_argument('--num_trajs', type=int, default=20)
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--dart', type=bool, default=False)
parser.add_argument('--dart_mu', type=float, default=0.0)
parser.add_argument('--dart_std', type=float, default=0.05)
parser.add_argument('--dart_samples', type=int, default=5)
args = parser.parse_args()

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

################################### TASK SETUP #################################

if args.task == 'pick_dry':
    config = pick_dry_config
elif args.task == 'pick_food':
    config = pick_food_config
elif args.task == 'pick_ripe':
    config = pick_ripe_config
elif args.mask == 'place_content':
    config = place_content_config
elif args.mask == 'place_stable':
    config = place_stable_config
elif args.mask == 'place_electronic':
    config = place_electronic_config
elif args.mask == 'sweep_hot':
    config = sweep_hot_config
elif args.mask == 'sweep_rug':
    config = sweep_rug_config
elif args.mask == 'sweep_sharp':
    config = sweep_sharp_config

env = vima_bench.make(task_name=config.task_name,task_kwargs=config.task_kwargs,record_gui=config.record_gui,hide_arm_rgb=config.hide_arm_rgb)

lang_model = SentenceTransformer('all-MiniLM-L6-v2', device=args.device)
lang_embed = lang_model.encode(config.lang_goal)

########################################################################

# generates random trajs within specified constraints
def gen_trajs(env, num_trajs, task_name, task_kwargs, goal, lga_phi_hat, ilga_phi_hat):
    trajs = []
    task = env.task
    oracle_fn = task.oracle(env)
    for traj in tqdm(range(num_trajs)):
        traj = {'obs': [], 'lga_obs': [], 'ilga_obs': [], 'obs_text': [], 'acts': [], 'goals':[], 'lang_goal': [], 'meta': []}
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
            segm = obs['segm']['top'] # extracts segm
            top_obs = obs['rgb']['top'] # extracts top down view only
            traj['obs'].append(process_obs(top_obs))
            traj['lga_obs'].append(process_segm(segm, lga_phi_hat, env.meta_info['obj_id_to_info']))
            traj['ilga_obs'].append(process_segm(segm, ilga_phi_hat, env.meta_info['obj_id_to_info']))
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
        traj['lga_obs'] = np.array(traj['lga_obs'])
        traj['ilga_obs'] = np.array(traj['ilga_obs'])
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

trajs = gen_trajs(env=env, num_trajs=args.num_trajs, task_name=config.task_name, task_kwargs=config.task_kwargs, goal=lang_embed, lga_phi_hat=config.lga_phi_hat, ilga_phi_hat=config.ilga_phi_hat)
pickle.dump(trajs, open(args.save_dir + '/trajs.pkl', 'wb'))
env.close()