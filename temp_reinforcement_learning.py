import gym
import gym_d2d

env = gym.make('D2DEnv-v0')

# obses = env.reset()
# game_over = False
# records = {}

# maxEpocs = 100
# bestResult = {}
# initialRewardCummulative = 0

for i in range(12):
    obses = env.reset()
    game_over = False
    records = {}

    maxEpocs = 100
    bestResult = {}
    initial_cummulative_reward_value = 0

    for epoc in range(maxEpocs):
        actions = {}
        for agent_id, obs in obses.items():
            action = env.action_space['due'].sample()  # or: action = agent.act(obs)
            actions[agent_id] = action

        obses, rewards, game_over, infos = env.step(actions)

        # for storing the {action, state , reward for each UE pair} 
        for key,value in actions.items():
            tx_rx_id_value = key
            current_reward = rewards[key]
            current_linktype = 1
            if(key[0] == 'd'):
                current_linktype = 3
            current_info = infos[tx_rx_id_value]
            current_sinr = current_info.get('sinr_db',None)
            current_snr = current_info.get('snr_db',None)
            current_rate = current_info.get('rate_bps',None)
            current_capacity = current_info.get('capacity_mbps',None)
            curr_pos = obses[tx_rx_id_value]
            current_position = {'tx': curr_pos[0], 'ty': curr_pos[1], 'rx':curr_pos[2], 'ry':curr_pos[3]}
            current_rb = current_info.get('rb',None)
            current_tx_pwr = current_info.get('tx_pwr_dbm',None)
            current_action = {'pos':current_position,'rb':current_rb,'tx_pwr_dbm':current_tx_pwr, 'linktype': current_linktype}
            current_state = {'sinr_db' : current_sinr , 'snr_db' : current_snr, 'rate_bps' : current_rate, 'capacity_mbps' : current_capacity}
            records[key] = {'action': current_action ,'state': current_state,'reward':current_reward}

            if(epoc != 0):
                bestResult_info = bestResult[key]
                bestReward = bestResult_info.get('reward',None)
                if(bestReward < current_reward):
                    bestResult[key] = records[key]

        if(epoc == 0):
            bestResult = records

            for key,value in records.items():
                reward_value = value.get('reward',None)
                initial_cummulative_reward_value += reward_value

    env.render()

    cummulative_reward_value = 0

    for key,value in bestResult.items():
        reward_value = value.get('reward',None)
        cummulative_reward_value += reward_value

    # print(f'The total reward (reinfocement learning) : {cummulative_reward_value}')
    print(f'initial value: {initial_cummulative_reward_value} and the final cummulative_reward_value {cummulative_reward_value}')