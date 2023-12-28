import math
import os
import pickle
import numpy as np
import cv2
import numpy as np

# function that, given an abstraction function and phi, returns phi_hat
def apply_abstraction(f, phi):
    phi_hat = []
    for obj in phi:
        if obj[0] in f.keys(): # if found obj
            if obj[1] in f[obj[0]]: # if found obj color
                phi_hat.append([obj[0], obj[1]])
    return phi_hat

def process_obs(obs):
    obs = np.rollaxis(obs,0,3)
    cv2.imwrite('temp.jpg', obs)
    img = cv2.imread('temp.jpg')
    processed_obs = cv2.resize(img, dsize=(72, 36), interpolation=cv2.INTER_CUBIC)
    return processed_obs

def process_segm(segm, phi_hat, env_obj_info):
    # searches if obj + properties are in phi_hat, keeps
    for obj in env_obj_info:
        if env_obj_info[obj]['obj_name'] in phi_hat.keys():
            if env_obj_info[obj]['texture_name'] in phi_hat[env_obj_info[obj]['obj_name']]:
                #import pdb; pdb.set_trace()
                segm[segm == obj] = 255
    # keeps phi_hat objs, masks out rest (arm=2)
    segm[segm != 255] = 0
    segm[segm == 255] = 1
    # reshape + resize
    segm = cv2.resize(segm, dsize=(72, 36), interpolation=cv2.INTER_LINEAR_EXACT)
    return segm

def process_raw_segm(segm):
    # converts all objs to mask
    segm[segm <= 1] = 0
    segm[segm > 1] = 1
    # reshape + resize
    segm = cv2.resize(segm, dsize=(72, 36), interpolation=cv2.INTER_LINEAR_EXACT)
    return segm

def flatten_act(action):
    return np.concatenate(list(action.values())).ravel()

# reconstructs actions for simulator
def reconstruct_act(action, env):
    reconst_action = {}
    reconst_action['pose0_position'] = np.array(action[0:2])
    reconst_action['pose0_rotation'] = np.array(action[2:6])
    reconst_action['pose1_position'] = np.array(action[6:8])
    reconst_action['pose1_rotation'] = np.array(action[8:12])
    reconst_action = {
        k: np.clip(v, env.action_space[k].low, env.action_space[k].high)
        for k, v in reconst_action.items()
    }
    return reconst_action

def compare_act(action1, action2):
    if np.linalg.norm(action1 - action2) < 0.2:
        return True
    return False

def remove_obj(segm, obs, remove_obj):
    #if remove_obj == 'arm':
    #    segm = (segm == 2).astype(int)
    if remove_obj == 'base':
        segm = (segm == 5).astype(int)
    elif remove_obj == 'dragged':
        segm = (segm == 6).astype(int)
    elif remove_obj == 'distractor':
        segm = (segm == 7).astype(int)
    segm = np.atleast_3d(segm)
    
    for height in range(128):
        for width in range(256):
            if segm[height, width] == 1:
                obs[height, width] = 47
    return obs

def compare_actions(actions, gt_action):
    comparisons = []
    for action in actions:
        comparisons.append(np.linalg.norm(gt_action - action[[0,1,6,7]],ord=2))
    return comparisons