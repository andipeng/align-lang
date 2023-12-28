import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable

class GCBCPolicy(nn.Module):
    def __init__(
        self, action_dim, hidden_size, output_mod=None):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=8, stride=4), nn.ReLU(inplace=True), nn.BatchNorm2d(32), #(b_size,3,36,72)=>(b_size,32,8,17)
            nn.Conv2d(32, 64, kernel_size=4, stride=2), nn.ReLU(inplace=True), nn.BatchNorm2d(64), #(b_size,32,8,17)=>(b_size,64,3,7)
            nn.Conv2d(64, 32, kernel_size=3, stride=1), nn.LeakyReLU(inplace=True), nn.BatchNorm2d(32), Flatten(), #(b_size,64,3,7)=>(b_size,32,1,5)=>(b_size,32*1*5)
            nn.Linear(32*1*5, hidden_size)#, nn.LeakyReLU(inplace=True), nn.BatchNorm1d(32), #(b_size,32*1*5)=>(b_size,action_dim)
        )
        self.policy = mlp(hidden_size+384, action_dim, hidden_dim=100, hidden_depth=1)
        self.apply(weight_init)

    def forward(self, state, goal):
        state = state/255.0 # process image + switch channels
        state = state.permute(0,3,1,2)
        state_embed = self.cnn(state)
        
        gc_embed = torch.cat([state_embed, goal], dim=1)
        action = self.policy(gc_embed)
        return action

class BCPolicy(nn.Module):
    def __init__(
        self, mask, input_dim, action_dim, hidden_size, output_mod=None):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(input_dim, 32, kernel_size=8, stride=4), nn.ReLU(inplace=True), nn.BatchNorm2d(32), #(b_size,3,36,72)=>(b_size,32,8,17)
            nn.Conv2d(32, 64, kernel_size=4, stride=2), nn.ReLU(inplace=True), nn.BatchNorm2d(64), #(b_size,32,8,17)=>(b_size,64,3,7)
            nn.Conv2d(64, 32, kernel_size=3, stride=1), nn.LeakyReLU(inplace=True), nn.BatchNorm2d(32), Flatten(), #(b_size,64,3,7)=>(b_size,32,1,5)=>(b_size,32*1*5)
            nn.Linear(32*1*5, action_dim)#, nn.LeakyReLU(inplace=True), nn.BatchNorm1d(32), #(b_size,32*1*5)=>(b_size,action_dim)
        )
        self.apply(weight_init)
        self.mask = mask

    def forward(self, state):
        if self.mask:
            state = state.unsqueeze(1)
        else:
            state = state/255.0 # process image + switch channels
            state = state.permute(0,3,1,2)
        action = self.cnn(state)
        return action

# Define simple MLP
class MLP(nn.Module):
    def __init__(
        self, input_dim, output_dim, hidden_dim, hidden_depth, final_act=None, output_mod=None
    ):
        super().__init__()
        self.trunk = mlp(input_dim, output_dim, hidden_dim, hidden_depth, final_act, output_mod)
        self.apply(weight_init)

    def forward(self, x):
        return self.trunk(x)

class Flatten(nn.Module):
    def forward(self, x):
        return x.reshape(x.size(0), -1)
    
def mlp(input_dim, output_dim, hidden_dim, hidden_depth, output_mod=None):
    if hidden_depth == 0:
        mods = [nn.Linear(input_dim, output_dim)]
    else:
        mods = [nn.Linear(input_dim, hidden_dim), nn.ReLU(inplace=True)]
        for i in range(hidden_depth - 1):
            mods += [nn.Linear(hidden_dim, hidden_dim), nn.ReLU(inplace=True)]
        mods.append(nn.Linear(hidden_dim, output_dim))
    if output_mod is not None:
        mods.append(output_mod)
    trunk = nn.Sequential(*mods)
    return trunk

# Custom weight init for Conv2D and Linear layers
def weight_init(m):
    if isinstance(m, nn.Linear):
        nn.init.orthogonal_(m.weight.data)
        if hasattr(m.bias, "data"):
            m.bias.data.fill_(0.0)