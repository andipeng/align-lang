import os
import numpy as np
import argparse
import matplotlib.pyplot as plt
import pickle
from tqdm import tqdm
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import distributions as pyd

from sentence_transformers import SentenceTransformer

from align_lang.policies import GCBCPolicy, BCPolicy
from align_lang.utils import process_obs, process_segm, reconstruct_act
from align_lang.configs.test import pick_config, place_config, rotate_config, sweep_config

import vima_bench

########################## VIDEO RECORD ####################################
record_cfg = {'save_video': True,
     'save_video_path': 'rollouts/',
     'view': 'front',
     'fps': 18,
     'video_height': 320,
     'video_width': 368}

parser = argparse.ArgumentParser()
parser.add_argument('--policy_dir', type=str, default='policies')
parser.add_argument('--policy', type=str, default='gcbc')
parser.add_argument('--task', type=str, default='pick')
parser.add_argument('--num_test_trajs', type=int, default=1)
parser.add_argument('--video', type=bool, default=True)
parser.add_argument('--device', type=str, default='cpu')

args = parser.parse_args()

################################### TASK SETUP #################################

if args.task == 'pick':
    config = pick_config
elif args.task == 'place':
    config = place_config
elif args.task == 'rotate':
    config = rotate_config
elif args.mask == 'sweep':
    config = sweep_config

env = vima_bench.make(task_name=config.task_name,task_kwargs=config.task_kwargs,record_cfg=record_cfg,hide_arm_rgb=config.hide_arm_rgb)

lang_model = SentenceTransformer('all-MiniLM-L6-v2', device=args.device)
lang_embed = lang_model.encode(config.lang_goal)

########################################################################

print("========================================")
print("Loading policy")
print("========================================")

policy = torch.load(args.policy_dir + '/' + args.policy + '_policy.pt', map_location=args.device)
policy.eval()

successes = []

for i in tqdm(range(args.num_test_trajs)):
    os.makedirs('rollouts/' + str(i), exist_ok=True)
    obs = env.reset()
    #obj_type = env.meta_info['obj_id_to_info'][6]['obj_name']
    
    if args.video:
        video_name = str(i)
        env.start_rec(video_name)
    for step in range(config.max_steps):
        # constructs s_hat from phi_hat
        segm = obs['segm']['top']
        s_hat = process_segm(segm, config.phi_hat, env.meta_info['obj_id_to_info'])
        im = Image.fromarray(s_hat.astype(np.uint8))
        im.save('rollouts/'+str(i)+"/"+str(step)+'_mask.jpg')
            
        # saves rgb image as well
        top_obs = obs['rgb']['top']
        top_obs = process_obs(top_obs)
        im = Image.fromarray(top_obs)
        im.save('rollouts/'+str(i)+"/"+str(step)+'.jpg')
            
        # uses either s_hat or true obs
        if args.policy == 'lga':
            state = s_hat
        else:
            state = top_obs
            
        state = torch.Tensor(state[None]).to(args.device)
        if args.policy == 'lga':
            action = policy(state).cpu().detach().numpy()[0]
        else:
            goal = torch.Tensor(lang_embed[None]).to(args.device)
            action = policy(state,goal).cpu().detach().numpy()[0]
            
        obs, _, done, info = env.step(action=reconstruct_act(action, env), skip_oracle=False)
        
    if done:
        successes.append(1)
    else:
        successes.append(0)
            
    if args.video:
        env.end_rec()
        
    # constructs s_hat from phi_hat
    segm = obs['segm']['top']
    s_hat = process_segm(segm, config.phi_hat, env.meta_info['obj_id_to_info'])
    im = Image.fromarray(s_hat.astype(np.uint8))
    im.save('rollouts/'+str(i)+"/"+str(step+1)+'_mask.jpg')
            
    # saves rgb image as well
    top_obs = obs['rgb']['top']
    top_obs = process_obs(top_obs)
    im = Image.fromarray(top_obs)
    im.save('rollouts/'+str(i)+"/"+str(step+1)+'.jpg')

env.close()

print("========================================")
print("Success Rate")
print("========================================")
print(sum(successes)/len(successes))