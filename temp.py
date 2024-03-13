import gym
import gym_d2d

env = gym.make('D2DEnv-v0')

obses = env.reset()
game_over = False
records = {}

while not game_over:
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

    env.render()

# FOR PRINTING THE CUMMULATIVE REWARD VALUE 

# cummulative_reward_value = 0

# for key,value in records.items():
#     reward_value = value.get('reward',None)
#     cummulative_reward_value += reward_value
    
# print(f'The total reward : {cummulative_reward_value}')
# print(cummulative_reward_value)
# FOR PRINTING THE COMPLETE INFORMATION OF ALL THE UE 

for record in records.items():
    print(record)





# FOR PRINTING THE GRAPH WITH COLORED NODES WITH SAME RESOURCE BLOCK
    
# from openpyxl import Workbook
    
# def save_to_excel(records):    
#     wb = Workbook()

#     ws = wb.active

#     headers = ['Key', 'tx', 'ty', 'rx', 'ry', 'linktype','rb','tx_pwr_dbm', 'sinr_db', 'snr_db', 'rate_bps', 'capacity_mbps','Reward']
#     ws.append(headers)

#     for key, value in records.items():
#         position_val = value['action'].get('pos')
#         row_data = [
#             key,
#             position_val.get('tx', ''),
#             position_val.get('ty', ''),
#             position_val.get('rx', ''),
#             position_val.get('ry', ''),
#             value['action'].get('linktype', ''),
#             value['action'].get('rb', ''),
#             value['action'].get('tx_pwr_dbm', ''),
#             value['state'].get('sinr_db', ''),
#             value['state'].get('snr_db', ''),
#             value['state'].get('rate_bps', ''),
#             value['state'].get('capacity_mbps', ''),
#             value['reward']
#         ]
#         ws.append(row_data)

#     wb.save("output_cueSinr.xlsx")

# save_to_excel(records)

# def plot_devices_rb(records,out_file: str = ''):
#     try:
#         import matplotlib.pyplot as plt
#     except ImportError:
#         raise ImportError('`plot_devices()` requires matplotlib')


    # due position grouped by rb
    # {rb -> {tx,ty}}
    # cue_rb = []
    # due_rb = []
    # colors = ['b', 'g', 'c', 'm', 'y', 'orange', 'purple', 'pink', 'brown', 'gold', 'lime', 'olive', 'teal', 'navy', 'indigo', 'maroon', 'tan', 'aqua', 'coral', 'darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkviolet', 'deeppink', 'goldenrod', 'khaki', 'lightblue', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightsteelblue', 'mediumaquamarine', 'mediumorchid', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'palegreen', 'paleturquoise', 'peru', 'plum', 'rosybrown', 'royalblue', 'sandybrown', 'seagreen', 'sienna', 'slateblue']

    # # cue position grouped by rb
    # for key,value in records.items():
    #     if(key[0] == 'c'):
    #         pos_val = value['action'].get('pos','')
    #         curr_rb = value['action'].get('rb','')
    #         cue_x = pos_val.get('tx','')
    #         cue_y = pos_val.get('ty','')
    #         rb_pos_val = {'rb':curr_rb,'x':cue_x,'y':cue_y}
    #         cue_rb.append(rb_pos_val)
    #     else:
    #         pos_val = value['action'].get('pos','')
    #         curr_rb = value['action'].get('rb','')
    #         due_tx_x = pos_val.get('tx','')
    #         due_tx_y = pos_val.get('ty','')
    #         rb_pos_val_tx = {'rb':curr_rb,'x':due_tx_x,'y':due_tx_y}
    #         due_rb.append(rb_pos_val_tx)
  
    #         due_rx_x = pos_val.get('rx','')
    #         due_rx_y = pos_val.get('ry','')
    #         rb_pos_val_rx = {'rb':curr_rb,'x':due_rx_x,'y':due_rx_y}
    #         due_rb.append(rb_pos_val_rx)
    
    # fig = plt.figure(figsize=(14, 7))
    # ax = fig.add_subplot(111)
    # mbs_pos_x = 0.0
    # mbs_pos_y = 0.0
    # ax.add_artist(plt.Circle((0,0), 500.0, color='b', alpha=0.1))
    
    # for data in cue_rb:
    #     rb_val = data.get('rb','')
    #     position_x = data.get('x','')
    #     position_y = data.get('y','')
    #     ax.scatter(position_x, position_y, c= colors[rb_val], label='CUE_TX')
        
    # for data in due_rb:
    #     rb_val = data.get('rb','')
    #     position_x = data.get('x','')
    #     position_y = data.get('y','')
    #     ax.scatter(position_x, position_y, c=colors[rb_val], label='DUE_TX')

    # ax.scatter(mbs_pos_x, mbs_pos_y, c='k', label='MBS')
    # ax.legend()
    # if out_file:
    #     plt.savefig(out_file)
    # plt.show()


# plot_devices_rb(records,'plot.png')

