import os
import numpy as np
import argparse
import matplotlib.pyplot as plt
import pickle

from sentence_transformers import SentenceTransformer
lang_model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

from align_lang.policies import GCBCPolicy, BCPolicy

parser = argparse.ArgumentParser()
parser.add_argument('--policy', type=str, default='GCBC')
parser.add_argument('--save_dir', type=str, default='/')
parser.add_argument('--data_dir', type=str, default='/expert_data')
parser.add_argument('--task', type=str, default='visual_manipulation')
parser.add_argument('--epochs', type=int, default=750)
parser.add_argument('--batch_size', type=int, default=10)
parser.add_argument('--hidden_layer_size', type=int, default=100)
parser.add_argument('--lr', type=int, default=0.001)

args = parser.parse_args()

if not os.path.exists(args.save_dir):
    os.mkdir(args.save_dir)

print("========================================")
print("Reading trajectories")
print("========================================")

obs_size = env.observation_space.shape[0]

trajs = pickle.load(open(args.data_dir + '/trajs.pkl', 'rb'))
act_size = trajs[0]['acts'][0].shape[0]

print("========================================")
print("Training Policy with %d trajectories" % len(trajs))
print("========================================")

if args.policy == 'GCBC'
    policy = GCBCPolicy(act_size, args.hidden_layer_size)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
policy.to(device)

criterion = nn.MSELoss()
optimizer = optim.Adam(list(policy.parameters()), lr=args.lr)

losses = []

idxs = np.array(range(len(trajs)))

num_batches = len(idxs) // args.batch_size
# Train the model with regular SGD
for epoch in range(args.num_epochs):  # loop over the dataset multiple times
    np.random.shuffle(idxs)
    running_loss = 0.0
    for i in range(num_batches):
        optimizer.zero_grad()

        t_idx = np.random.randint(len(trajs), size=(batch_size,)) # Indices of traj
        t_idx_pertraj = np.random.randint(1, size=(batch_size,)) # Indices of timesteps in traj
        t_states = np.concatenate([trajs[c_idx]['obs'][t_idx][None] for (c_idx, t_idx) in zip(t_idx, t_idx_pertraj)])
        t_goals = np.concatenate([trajs[c_idx]['goals'][t_idx][None] for (c_idx, t_idx) in zip(t_idx, t_idx_pertraj)])
        t_actions = np.concatenate([trajs[c_idx]['acts'][t_idx][None] for (c_idx, t_idx) in zip(t_idx, t_idx_pertraj)])
   
        t_states = torch.Tensor(t_states).float().to(device)
        t_goals = torch.Tensor(t_goals).float().to(device)
        t_actions = torch.Tensor(t_actions).float().to(device)
        
        #a_preds = policy(t_states, t_goals)
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

torch.save(policy, 'policy.pt')
print('Finished Training')

plt.plot(losses)
plt.savefig(self.save_dir + '/training_loss.png')