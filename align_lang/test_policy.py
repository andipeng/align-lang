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
from align_lang.utils import process_obs, process_segm, process_raw_segm, reconstruct_act
from align_lang.configs.test.iclr import red_heart_config
from align_lang.configs.test.hri import pick_dry_config, pick_food_config, pick_ripe_config, place_content_config, place_electronic_config, place_stable_config, sweep_hot_config, sweep_rug_config, sweep_sharp_config

import vima_bench

parser = argparse.ArgumentParser()
parser.add_argument('--policy_dir', type=str, default='policies')
parser.add_argument('--policy', type=str, default='gcbc') # gcbc, gcbc_segm, lga, lga_hill, human, ilga
parser.add_argument('--task', type=str, default='red_heart')
parser.add_argument('--num_test_trajs', type=int, default=5)
parser.add_argument('--video', type=bool, default=True)
parser.add_argument('--device', type=str, default='cpu')

args = parser.parse_args()

########################## VIDEO RECORD ####################################
record_cfg = {'save_video': True,
     'save_video_path': 'rollouts/'+args.policy,
     'view': 'front',
     'fps': 18,
     'video_height': 320,
     'video_width': 368}

################################### TASK SETUP #################################

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
    os.makedirs('rollouts/' + args.policy + str(i), exist_ok=True)
    obs = env.reset()
    #obj_type = env.meta_info['obj_id_to_info'][6]['obj_name']
    
    if args.video:
        video_name = str(i)
        env.start_rec(video_name)
    for step in range(config.max_steps):
        # constructs s_hat from phi_hat
        segm = obs['segm']['top']
        if args.policy == "lga":
            s_hat = process_segm(segm.copy(), config.lga_phi_hat, env.meta_info['obj_id_to_info'])
            s_hat_save = s_hat*255
            im = Image.fromarray(s_hat_save.astype(np.uint8))
            im.save('rollouts/'+ args.policy + str(i)+"/"+str(step)+'_lga_shat.jpg')
        elif args.policy == 'gcbc_segm':
            s_hat = process_raw_segm(segm.copy())
            s_hat_save = s_hat*255
            im = Image.fromarray(s_hat_save.astype(np.uint8))
            im.save('rollouts/'+ args.policy + str(i)+"/"+str(step)+'_segm.jpg')
        elif args.policy == "lga_hill":
            s_hat = process_segm(segm.copy(), config.lga_hill_phi_hat, env.meta_info['obj_id_to_info'])
            s_hat_save = s_hat*255
            im = Image.fromarray(s_hat_save.astype(np.uint8))
            im.save('rollouts/'+ args.policy + str(i)+"/"+str(step)+'_lga_hill_shat.jpg')
        elif args.policy == "human":
            s_hat = process_segm(segm.copy(), config.human_phi_hat, env.meta_info['obj_id_to_info'])
            s_hat_save = s_hat*255
            im = Image.fromarray(s_hat_save.astype(np.uint8))
            im.save('rollouts/'+ args.policy + str(i)+"/"+str(step)+'_human_shat.jpg')
        elif args.policy == "ilga":
            s_hat = process_segm(segm.copy(), config.ilga_phi_hat, env.meta_info['obj_id_to_info'])
            s_hat_save = s_hat*255
            im = Image.fromarray(s_hat_save.astype(np.uint8))
            im.save('rollouts/'+ args.policy + str(i)+"/"+str(step)+'_ilga_shat.jpg')
            
        # saves rgb image as well
        top_obs = obs['rgb']['top']
        top_obs = process_obs(top_obs)
        im = Image.fromarray(top_obs)
        im.save('rollouts/'+ args.policy + str(i)+"/"+str(step)+'_obs.jpg')
            
        # uses either s_hat (potentially segm) or true obs
        if args.policy == 'gcbc':
            state = top_obs
        else:
            state = s_hat
            
        state = torch.Tensor(state[None]).to(args.device)
        if args.policy == 'gcbc':
            goal = torch.Tensor(lang_embed[None]).to(args.device)
            action = policy(state,goal).cpu().detach().numpy()[0]
        else:
            action = policy(state).cpu().detach().numpy()[0]
        obs, _, done, info = env.step(action=reconstruct_act(action, env), skip_oracle=False)
        
    if done:
        successes.append(1)
    else:
        successes.append(0)
            
    if args.video:
        env.end_rec()
        
    # constructs s_hat from phi_hat
    segm = obs['segm']['top']
    if args.policy == "lga":
        s_hat = process_segm(segm.copy(), config.lga_phi_hat, env.meta_info['obj_id_to_info'])
        s_hat_save = s_hat*255
        im = Image.fromarray(s_hat_save.astype(np.uint8))
        im.save('rollouts/'+ args.policy + str(i)+"/"+str(step+1)+'_lga_shat.jpg')
    elif args.policy == 'gcbc_segm':
        s_hat = process_raw_segm(segm.copy())
        s_hat_save = s_hat*255
        im = Image.fromarray(s_hat_save.astype(np.uint8))
        im.save('rollouts/'+ args.policy + str(i)+"/"+str(step+1)+'_segm.jpg')
    elif args.policy == "lga_hill":
        s_hat = process_segm(segm.copy(), config.lga_hill_phi_hat, env.meta_info['obj_id_to_info'])
        s_hat_save = s_hat*255
        im = Image.fromarray(s_hat_save.astype(np.uint8))
        im.save('rollouts/'+ args.policy + str(i)+"/"+str(step+1)+'_lga_hill_shat.jpg')
    elif args.policy == "human":
        s_hat = process_segm(segm.copy(), config.human_phi_hat, env.meta_info['obj_id_to_info'])
        s_hat_save = s_hat*255
        im = Image.fromarray(s_hat_save.astype(np.uint8))
        im.save('rollouts/'+ args.policy + str(i)+"/"+str(step+1)+'_human_shat.jpg')
    elif args.policy == "ilga":
        s_hat = process_segm(segm.copy(), config.ilga_phi_hat, env.meta_info['obj_id_to_info'])
        s_hat_save = s_hat*255
        im = Image.fromarray(s_hat_save.astype(np.uint8))
        im.save('rollouts/'+ args.policy + str(i)+"/"+str(step+1)+'_ilga_shat.jpg')
            
    # saves rgb image as well
    top_obs = obs['rgb']['top']
    top_obs = process_obs(top_obs.copy())
    im = Image.fromarray(top_obs)
    im.save('rollouts/'+ args.policy + str(i)+"/"+str(step+1)+'_obs.jpg')

env.close()

print("========================================")
print("Success Rate")
print("========================================")
print(sum(successes)/len(successes))