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
from align_lang.utils import downsize_obs, reconstruct_act

import vima_bench

########################## TASK DEF ####################################

visual_man_task_kwargs = {'num_dragged_obj': 1,
     'num_base_obj': 1,
     'num_other_obj': 0,
     'dragged_obj_loc': [1],
     'base_obj_loc': [4],
     'third_obj_loc' : [1],
     'fourth_obj_loc' : [3],
     'possible_dragged_obj': ['bowl'],
     'possible_dragged_obj_texture': ['red'],
     'possible_base_obj': ['pan'],
     'possible_base_obj_texture': ['blue'],
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

########################## VIDEO RECORD ####################################

record_cfg = {'save_video': True,
     'save_video_path': 'rollouts/',
     'view': 'front',
     'fps': 18,
     'video_height': 320,
     'video_width': 368}

########################## VIDEO RECORD ####################################

parser = argparse.ArgumentParser()
parser.add_argument('--policy_dir', type=str, default='results')
parser.add_argument('--task', type=str, default='visual_manipulation')
parser.add_argument('--num_test_trajs', type=int, default=1)
parser.add_argument('--video', type=bool, default=True)
parser.add_argument('--max_steps', type=int, default=1)
parser.add_argument('--device', type=str, default='cpu')

args = parser.parse_args()

########################## LANG DEF ####################################

lang_model = SentenceTransformer('all-MiniLM-L6-v2', device=args.device)
lang_goal = 'bring me the bowl'
lang_embed = lang_model.encode(lang_goal)

########################################################################

#record_gui=True, display_debug_window=True, hide_arm_rgb=False
if args.task == 'visual_manipulation':
    task_kwargs = visual_man_task_kwargs
    env = vima_bench.make(task_name=args.task,task_kwargs=task_kwargs,hide_arm_rgb=False,record_cfg=record_cfg)
elif args.task == 'rotate':
    task_kwargs = rotate_task_kwargs
    env = vima_bench.make(task_name=args.task,task_kwargs=rotate_task_kwargs,hide_arm_rgb=False,record_cfg=record_cfg)
elif args.task == 'sweep_without_touching':
    task_kwargs = sweep_task_kwargs
    env = vima_bench.make(task_name=args.task,task_kwargs=sweep_task_kwargs,hide_arm_rgb=False,record_cfg=record_cfg)

print("========================================")
print("Loading policy")
print("========================================")

policy = torch.load(args.policy_dir + '/policy.pt', map_location=args.device)
policy.eval()

successes = []

for i in tqdm(range(args.num_test_trajs)):
    os.makedirs('rollouts/' + str(i), exist_ok=True)
    obs = env.reset()
    obj_type = env.meta_info['obj_id_to_info'][6]['obj_name']
    goal_embed = lang_model.encode(obj_type)
    
    if args.video:
        video_name = str(i)
        env.start_rec(video_name)
    for step in range(args.max_steps):
        segm = obs['segm']['top']
        top_obs = obs['rgb']['top']
        top_obs = np.rollaxis(top_obs,0,3)

        first_obs = top_obs.copy()

        im = Image.fromarray(top_obs)
        im.save('rollouts/'+str(i)+"/"+str(step)+'.jpg')
        top_obs = downsize_obs(top_obs)
        state = torch.Tensor(top_obs[None]).to(args.device)
        goal = torch.Tensor(lang_embed[None]).to(args.device)
        action = policy(state,goal).cpu().detach().numpy()[0] #GCBC
        #action = policy(state).cpu().detach().numpy()[0] #BC

        obs, _, done, info = env.step(action=reconstruct_act(action, env), skip_oracle=False)
        segm = obs['segm']['top']
        
    if done:
        successes.append(1)
    else:
        successes.append(0)
            
    if args.video:
        env.end_rec()
        
    top_obs = obs['rgb']['top']
    top_obs = np.rollaxis(top_obs,0,3)
        
    im = Image.fromarray(top_obs)
    im.save('rollouts/'+str(i)+"/"+str(step+1)+'.jpg')

env.close()

print("========================================")
print("Success Rate")
print("========================================")
print(sum(successes)/len(successes))