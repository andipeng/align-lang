import math
import os
import pickle
import numpy as np

def downsize_obs(obs):
    cv2.imwrite('temp.jpg', obs)
    img = cv2.imread('temp.jpg')
    downsized_obs = cv2.resize(img, dsize=(72, 36), interpolation=cv2.INTER_CUBIC)
    return downsized_obs

def flatten_act(action):
    return np.concatenate(list(action.values())).ravel()

# reconstructs actions for simulator
def reconstruct_act(action):
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