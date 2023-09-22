import os
import numpy as np
import argparse
import pickle
import random

from align_lang.utils import apply_abstraction, compare_act
from align_lang.lm_experiments.ilga import pick_ripe
from align_lang.configs.train import pick_config, place_config, rotate_config, sweep_config

parser = argparse.ArgumentParser()
parser.add_argument('--task', type=str, default='pick') # gcbc, bc, lga
parser.add_argument('--hidden_pref', type=str, default='ripe')
parser.add_argument('--save_dir', type=str, default='ilga')
parser.add_argument('--data_dir', type=str, default='expert_data')
parser.add_argument('--num_traj_pairs', type=int, default=1)

args = parser.parse_args()

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

if args.task == 'pick':
    config = pick_config
elif args.task == 'place':
    config = place_config
elif args.task == 'rotate':
    config = rotate_config
elif args.mask == 'sweep':
    config = sweep_config

print("========================================")
print("Reading trajectories")
print("========================================")

trajs = pickle.load(open(args.data_dir + '/trajs.pkl', 'rb'))
lang_goal = trajs['lang_goal']

print("========================================")
print("Interative LGA")
print("========================================")

abs_func = config.phi_hat # initialize with LGA
theta_star = {} # prefs to add 

for i in range(args.num_traj_pairs):
    traj1 = random.choice(trajs) # sample 2 trajs + initial states
    traj2 = random.choice(trajs)
    traj1_phi_hat = apply_abstraction(abs_func, traj1['obs_text'])
    traj2_phi_hat = apply_abstraction(abs_func, traj2['obs_text'])

    # enter ILGA if abstractions are same but actions different
    if traj1_phi_hat == traj2_phi_hat and not compare_act(traj1['acts'][0], traj2['acts'][0]):
        delta_phi = np.setdiff1d(traj1['obs_text'] - traj2['obs_text']) # find set diff between states

        # query LM for prefs, add if over epsilon
        prefs = query_preference(lang_goal, delta_phi)
        for pref in prefs:
            if pref['score'] > config.epsilon
                theta_star.add(pref['preference'])
        
        # if we didn't find a preference, query human
        if len(theta_star) == 0:
            prefs = query_preference_human()
            theta_star.add(prefs)

        # update with the lang goal + human prefs
        abs_func = update_abstraction(lang_goal, theta_star)

torch.save(abs_func, args.save_dir + '/' + args.task + args.hidden_pref + '_phi_hat.txt')
print('Finished Training')