import numpy as np
import tensorflow as tf
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from collections import deque
from gym_d2d.envs.env_config import EnvConfig as config
from keras.layers import Input


import gym
import gym_d2d

class DQN:
    def __init__(self,state_size,action_size,learning_rate):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.gamma = .95
        self.replay_memory = deque(maxlen = 2000)
        self.model = self.build_model()

        self.target_model = self.build_model()
        self.update_target_weights()

    def build_model(self):
        model = Sequential()   
        model.add(Input(shape=(self.state_size,)))  
        model.add(Dense(32, activation="relu"))
        model.add(Dense(64,activation="relu"))
        model.add(Dense(self.action_size,activation="linear"))
        model.compile(loss="mse",optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def act(self,state):
        if np.random.rand() <= self.epsilon:
            return random.choice([rb for rb in range(self.action_size // (config.due_max_tx_power_dBm - config.due_min_tx_power_dBm + 1)) for pt in range(self.action_size % (config.due_max_tx_power_dBm - config.due_min_tx_power_dBm + 1))])
        q_values = self.model.predict(state[np.newaxis])  # predict Q values for the state
        return np.argmax(q_values[0])  # return action (resource block , power) with highest Q value

    def store(self,state,action,reward,next_state,done):
        self.replay_memory.append((state,action,reward,next_state,done))

    def train(self,batch_size):
        if len(self.replay_memory) < batch_size:
            return
        
        minibatch = random.sample(self.replay_memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*minibatch)
        states = np.array(states)
        next_states = np.array(next_states)
        actions = np.array(actions)

        resource_blocks, power_levels = zip(*actions)

        target_q_values = self.target.model.predict(next_states)
        target_q_values[dones] = 0 # set Target Q values to zero for terminal states
        expected_q_values = rewards + self.gamma * np.amax(target_q_values,axis=1)

        states = np.concatenate((states,resource_blocks[:,np.newaxis], power_levels[:,np.newaxis]), axis=1)
        expected_q_values = expected_q_values.reshape(-1,1)

        loss = self.model.train_on_batch(states,expected_q_values)

        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, 0.01)   # minimum exploration rate

    def update_target_weights(self):
        self.target_model.set_weights(self.model.get_weights())

env = gym.make('D2DEnv-v0')

obses = env.reset()
game_over = False
records = {}

state_size = 10000
action_size = 200

learning_rate = 0.1

agent = DQN(state_size,action_size,learning_rate)
episodes = 10

for episode in range(episodes):
    done = False
    episode_reward = 0

    while not done:
        state = obses
        print(state)
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        episode_reward += reward

        # store replay_memory
        agent.store(state,action,reward,next_state,done)
        
        # train the agent using replay memory
        agent.train()

        obs_state = next_state
    
    print(f"Episode: {episode+1}, Reward: {episode_reward}")