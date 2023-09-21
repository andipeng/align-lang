import os
import numpy as np
import argparse
import matplotlib.pyplot as plt
import pickle

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch import distributions as pyd

from sentence_transformers import SentenceTransformer

from align_lang.policies import GCBCPolicy, BCPolicy

parser = argparse.ArgumentParser()
parser.add_argument('--policy', type=str, default='GCBC') # GCBC, BC, LGA
parser.add_argument('--save_dir', type=str, default='policies')
parser.add_argument('--data_dir', type=str, default='expert_data')
parser.add_argument('--task', type=str, default='visual_manipulation')
parser.add_argument('--epochs', type=int, default=750)
parser.add_argument('--batch_size', type=int, default=10)
parser.add_argument('--hidden_layer_size', type=int, default=100)
parser.add_argument('--lr', type=int, default=0.001)
parser.add_argument('--device', type=str, default='cpu')

args = parser.parse_args()

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

print("========================================")
print("Reading trajectories")
print("========================================")

trajs = pickle.load(open(args.data_dir + '/trajs.pkl', 'rb'))
act_size = trajs[0]['acts'][0].shape[0]

print("========================================")
print("Training Policy with %d trajectories" % len(trajs))
print("========================================")

if args.policy == 'GCBC':
    policy = GCBCPolicy(act_size, args.hidden_layer_size)
else:
    policy = BCPolicy(act_size, args.hidden_layer_size)
policy.to(args.device)

criterion = nn.MSELoss()
optimizer = optim.Adam(list(policy.parameters()), lr=args.lr)

losses = []

idxs = np.array(range(len(trajs)))

num_batches = len(idxs) // args.batch_size
# Train the model with regular SGD
for epoch in range(args.epochs):  # loop over the dataset multiple times
    np.random.shuffle(idxs)
    running_loss = 0.0
    for i in range(num_batches):
        optimizer.zero_grad()

        t_idx = np.random.randint(len(trajs), size=(args.batch_size,)) # Indices of traj
        t_idx_pertraj = np.random.randint(1, size=(args.batch_size,)) # Indices of timesteps in traj
        if args.policy == 'LGA':
            t_states = np.concatenate([trajs[c_idx]['mask_obs'][t_idx][None] for (c_idx, t_idx) in zip(t_idx, t_idx_pertraj)])
        else:
            t_states = np.concatenate([trajs[c_idx]['obs'][t_idx][None] for (c_idx, t_idx) in zip(t_idx, t_idx_pertraj)])
        t_goals = np.concatenate([trajs[c_idx]['goals'][t_idx][None] for (c_idx, t_idx) in zip(t_idx, t_idx_pertraj)])
        t_actions = np.concatenate([trajs[c_idx]['acts'][t_idx][None] for (c_idx, t_idx) in zip(t_idx, t_idx_pertraj)])
   
        t_states = torch.Tensor(t_states).float().to(args.device)
        t_goals = torch.Tensor(t_goals).float().to(args.device)
        t_actions = torch.Tensor(t_actions).float().to(args.device)
        
        if args.policy == 'GCBC':
            a_preds = policy(t_states, t_goals)
        else:
            a_preds = policy(t_states)
        loss = torch.mean(torch.linalg.norm(a_preds - t_actions, dim=-1)) # supervised learning loss
        
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 100 == 0:
            print('[%d, %5d] loss: %.8f' %
                  (epoch + 1, i + 1, running_loss))
            losses.append(running_loss)
            running_loss = 0.0
        losses.append(loss.item())

torch.save(policy, args.save_dir + '/' + args.policy + '_policy.pt')
print('Finished Training')

plt.plot(losses)
plt.savefig(args.save_dir + '/training_loss.png')