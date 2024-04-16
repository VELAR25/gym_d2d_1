import gym 
import time
import torch 
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Any

@dataclass
class Sars:
    state: Any
    action: int
    reward: float
    next_state: Any

class DQNAgent:
    def __init__(self,model):
        self.model = model

    def get_actions(self,observations):
        # observations shape -> (N,4) -> change 4(velocity, polevelocity,x,y) as per D2D 
        q_vals = self.model(observations)

        # q_vals shape(N,2) -> 2 -> no of actions 
        return q_vals.max(-1)
    
class Model(nn.Module):
    def __init__(self, obs_shape, num_actions):
        super(Model,self).__init__()
        assert len(obs_shape) == 1 # will work for flat observations only
        self.obs_space = obs_shape
        self.num_actions = num_actions
        self.net = torch.nn.Sequential(
            torch.nn.Linear(obs_shape[0], 256),
            torch.nn.ReLU(), 
            torch.nn.Linear(256,num_actions),
        )

    def forward(self,x):
        return self.net(x)
    
class ReplayBuffer:
    def __init__(self, buffer_size = 100000):
        self.buffer_size = buffer_size
        self.buffer = []

    def insert(self,sars):
        self.buffer.append(sars)
        self.buffer = self.buffer[-self.buffer_size:]
    
    def sample(self,num_samples):
        assert num_samples <= len(self.buffers)
        return sample(self.buffer, num_samples)