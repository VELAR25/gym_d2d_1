from pathlib import Path

import gym
import gym_d2d

# env = gym.make('D2DEnv-v0')

# obses = env.reset()  # generate random device positions (if not supplied)
# env.save_device_config(Path.cwd() / 'device_config.json')

env_config = {'device_config_file': Path.cwd() / 'device_config.json'}
env = gym.make('D2DEnv-v0', env_config=env_config)

game_over = False
while not game_over:
    actions = {}
    # for agent_id, obs in obses.items():
    #     action = env.action_space['due'].sample()  # or: action = agent.act(obs)
    #     actions[agent_id] = action

    obses, rewards, game_over, infos = env.step(actions)
    env.render()