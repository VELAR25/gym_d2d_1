import gym
import gym_d2d

env = gym.make('D2DEnv-v0')

obses = env.reset()
game_over = False
while not game_over:
    actions = {}
    for agent_id, obs in obses.items():
        action = env.action_space['due'].sample()  # or: action = agent.act(obs)
        actions[agent_id] = action

    obses, rewards, game_over, infos = env.step(actions)
    env.render()