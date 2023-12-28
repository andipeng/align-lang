import os
import numpy as np
import argparse
import pickle
import random

from align_lang.utils import apply_abstraction, compare_act
from align_lang.configs.train.hri import pick_dry_config, pick_food_config, pick_ripe_config, place_content_config, place_electronic_config, place_stable_config, sweep_hot_config, sweep_rug_config, sweep_sharp_config

parser = argparse.ArgumentParser()
parser.add_argument('--task', type=str, default='pick_dry')
parser.add_argument('--hidden_pref', type=str, default='ripe')
parser.add_argument('--save_dir', type=str, default='ilga')
parser.add_argument('--data_dir', type=str, default='expert_data')
parser.add_argument('--num_traj_pairs', type=int, default=1)

args = parser.parse_args()

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

if args.task == 'pick_dry':
    config = pick_dry_config
elif args.task == 'pick_food':
    config = pick_food_config
elif args.task == 'pick_ripe':
    config = pick_ripe_config
elif args.task == 'place_content':
    config = place_content_config
elif args.task == 'place_stable':
    config = place_stable_config
elif args.task == 'place_electronic':
    config = place_electronic_config
elif args.task == 'sweep_hot':
    config = sweep_hot_config
elif args.task == 'sweep_rug':
    config = sweep_rug_config
elif args.task == 'sweep_sharp':
    config = sweep_sharp_config
elif args.task == 'red_heart':
    config = red_heart_config

print("========================================")
print("Reading trajectories")
print("========================================")

trajs = pickle.load(open(args.data_dir + '/trajs.pkl', 'rb'))
lang_goal = trajs['lang_goal']

print("========================================")
print("Interative LGA")
print("========================================")

abs_func = config.lga_phi_hat

for i in range(args.num_traj_pairs):
    traj1 = random.choice(trajs) # sample 2 trajs + initial states
    traj2 = random.choice(trajs)
    traj1_phi_hat = apply_abstraction(abs_func, traj1['obs_text'])
    traj2_phi_hat = apply_abstraction(abs_func, traj2['obs_text'])

    # if abstractions are same but actions different
    if traj1_phi_hat == traj2_phi_hat and not compare_act(traj1['acts'][0], traj2['acts'][0]):
        delta_phi = np.setdiff1d(traj1['obs_text'] - traj2['obs_text']) # find set diff between states

        print(traj1['obs_text'])
        print(traj2['obs_text'])
        print(delta_phi)