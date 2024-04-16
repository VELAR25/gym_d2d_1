import gym
import gym_d2d
import math

env = gym.make('D2DEnv-v0')

# obses = env.reset()
# game_over = False
# records = {}

# maxEpocs = 100
# bestResult = {}
# initialRewardCummulative = 0

# FOR PRINTING THE GRAPH WITH COLORED NODES WITH SAME RESOURCE BLOCK

import plotly.graph_objects as go
import numpy as np

from openpyxl import Workbook

wb = Workbook()
ws = wb.active

def distance_between_UE_pairs(x1,y1,x2,y2) -> float:
    return math.sqrt(pow(x1-x2,2) + pow(y1-y2,2))
    
def initialize_excel_with_headers():

    headers = ['Key', 'tx', 'ty', 'rx', 'ry', 'linktype','rb','tx_pwr_dbm', 'sinr_db', 'snr_db', 'rate_bps', 'capacity_mbps','reward','initial_cummulative_reward','best_cummulative_reward']
    ws.append(headers)

def save_to_excel(records,name_of_file):    
   
    for key, value in records.items():
        if(type(value) != list):
            position_val = value['action'].get('pos')
            row_data = [
                key,
                position_val.get('tx', ''),
                position_val.get('ty', ''),
                position_val.get('rx', ''),
                position_val.get('ry', ''),
                value['action'].get('linktype', ''),
                value['action'].get('rb', ''),
                value['action'].get('tx_pwr_dbm', ''),
                value['state'].get('sinr_db', ''),
                value['state'].get('snr_db', ''),
                value['state'].get('rate_bps', ''),
                value['state'].get('capacity_mbps', ''),
                value['reward'],
                value["initial_cummulative_reward"],
                value["best_cummulative_reward"]
            ]
            ws.append(row_data)
        else:
            for i in range(len(value)):
                key_value = value[i]
                position_val = key_value['action'].get('pos')
                row_data = [
                    key,
                    position_val.get('tx', ''),
                    position_val.get('ty', ''),
                    position_val.get('rx', ''),
                    position_val.get('ry', ''),
                    key_value['action'].get('linktype', ''),
                    key_value['action'].get('rb', ''),
                    key_value['action'].get('tx_pwr_dbm', ''),
                    key_value['state'].get('sinr_db', ''),
                    key_value['state'].get('snr_db', ''),
                    key_value['state'].get('rate_bps', ''),
                    key_value['state'].get('capacity_mbps', ''),
                    key_value['reward'],
                    key_value["initial_cummulative_reward"],
                    key_value["best_cummulative_reward"]
                ]
                ws.append(row_data)

    wb.save(name_of_file + ".xlsx")

# CODE FOR PLOTTING THE REWARD VALUES 
reward_value_collection = []

for i in range(1):
    print(i)
    obses = env.reset()
    game_over = False
    records = {}

    determine_color = {}
    maxEpisodes = 200
    bestResult = {}
    initial_cummulative_reward_value = 0
    best_cummulative_reward_value = 0
    cue_details_for_graph = {}
    due_details_for_graph = {}
    neighborsInfo = {}
    ue_devices_range = 40.0

    if(i == 0):
        initialize_excel_with_headers()

    for episode in range(maxEpisodes):
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
        
        if(episode == 0):
            bestResult = records

            for key,value in records.items():
                reward_value = value.get('reward',None)
                initial_cummulative_reward_value += reward_value

            best_cummulative_reward_value = initial_cummulative_reward_value

            reward_value_collection.append(initial_cummulative_reward_value) 

        else:
            cummulative_reward_value = 0
            no_negative_reward = True
            for key,value in records.items():
                reward_value = value.get('reward',None)
                if(reward_value < 0):
                    no_negative_reward = False
                cummulative_reward_value += reward_value
                
            if(no_negative_reward == True and best_cummulative_reward_value < cummulative_reward_value):
                best_cummulative_reward_value = cummulative_reward_value
                bestResult = records 

            reward_value_collection.append(cummulative_reward_value)

    for key,value in bestResult.items():
    
        # STORING THE NEIGHBORS INFORMATION 
        current_ue_id = key 
        x_pos = value.get('action',"None").get("pos","None").get("tx","None")
        y_pos = value.get('action',"None").get("pos","None").get("ty","None")
        
        # iterating inside the circle of current UE to gather information of its neighbor
        
        for keyNeigh, valueNeigh in bestResult.items():
            if(key != keyNeigh):
                neighbor_x_pos = valueNeigh.get('action',"None").get("pos","None").get("tx","None")
                neighbor_y_pos = valueNeigh.get('action',"None").get("pos","None").get("ty","None")

                  
                if(distance_between_UE_pairs(x_pos,y_pos,neighbor_x_pos,neighbor_y_pos) <= ue_devices_range):
                    if current_ue_id in neighborsInfo:
                        neighborsInfo[current_ue_id].append(valueNeigh)
                    else:
                        neighborsInfo[current_ue_id] = []
                        neighborsInfo[current_ue_id].append(valueNeigh)
        

        bestResult[key]['initial_cummulative_reward'] = initial_cummulative_reward_value
        bestResult[key]['best_cummulative_reward'] = best_cummulative_reward_value
        
        # pos_key = (0,0)
        # pos_key1 = (0,0)
        # pos_key2 = (0,0)

        # if(key[0] == 'c'):
        #     pos_key = (bestResult[key]["action"]["pos"]["tx"], bestResult[key]["action"]["pos"]["ty"])
        # else:
        #     pos_key1 = (bestResult[key]["action"]["pos"]["tx"], bestResult[key]["action"]["pos"]["ty"])
        #     pos_key2 = (bestResult[key]["action"]["pos"]["rx"], bestResult[key]["action"]["pos"]["ry"])

        # colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'lightpink', 'white', 'gray', 'silver', 'navajowhite', 'skyblue', 'chocolate', 'darkcyan', 'darkmagenta', 'darkolivegreen', 'darkorchid', 'darkslategray', 'darkturquoise', 'firebrick', 'forestgreen', 'fuchsia', 'hotpink', 'indianred', 'lawngreen', 'lightcoral', 'lightgoldenrodyellow', 'lightgrey', 'lightseagreen', 'lightslategray', 'lightyellow', 'limegreen', 'mediumblue', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumvioletred', 'navy', 'olivedrab', 'orangered', 'palevioletred', 'peru', 'powderblue', 'salmon', 'seashell', 'sienna']

        
        # if(key[0] == 'c'):
        #     determine_color[pos_key] = colors[bestResult[key]["action"]["rb"]]
        # else:
        #     determine_color[pos_key1] = colors[bestResult[key]["action"]["rb"]]
        #     determine_color[pos_key2] = colors[bestResult[key]["action"]["rb"]]

        split_ids = key.split(":")
        first_ue = split_ids[0]
        second_ue = split_ids[1]
        if(key[0] == "c"):
            cue_details_for_graph[first_ue] = {"tx": bestResult[key]["action"]["pos"]["tx"],"ty" :bestResult[key]["action"]["pos"]["ty"],"rb":bestResult[key]["action"]["rb"],"linktype":bestResult[key]["action"]["linktype"],"reward":bestResult[key]["reward"]}
        else: 
            due_details_for_graph[first_ue] = {"tx": bestResult[key]["action"]["pos"]["tx"],"ty" :bestResult[key]["action"]["pos"]["ty"],"rb":bestResult[key]["action"]["rb"],"linktype":bestResult[key]["action"]["linktype"],"reward":bestResult[key]["reward"]}
            due_details_for_graph[second_ue] = {"tx": bestResult[key]["action"]["pos"]["rx"],"ty" :bestResult[key]["action"]["pos"]["ry"],"rb":bestResult[key]["action"]["rb"],"linktype":bestResult[key]["action"]["linktype"],"reward":bestResult[key]["reward"]}

    
    # SAVING THE BEST RESULT TO A EXCEL FILE 
    save_to_excel(bestResult,"output_data")

    # SAVING THE NEIGHBOR INFORMATION TO A EXCEL FILE 
    save_to_excel(neighborsInfo,"neighbors_information")

    env.render()
    
    # PLOTTING THE GRAPH FOR REWARD VALUE COLLECTION 

    import matplotlib.pyplot as plt

    # Assuming your array is named 'arr'
    plt.plot(range(1, len(reward_value_collection) + 1), reward_value_collection)  # Use range(1, len(arr) + 1) for x-axis from 1

    # Set labels and title for the plot
    plt.xlabel("Episode")
    plt.ylabel("Reward Value")
    plt.title("Plotting the Reward Value with each Episode")

    # Display the plot
    plt.show()

"""
    # D2D communication points with properties (sample data)
    
    # Extract x and y coordinates for cue pairs 
    cue_x_values = [cue_details_for_graph[key]["tx"] for key,value in cue_details_for_graph.items()]
    cue_y_values = [cue_details_for_graph[key]["ty"] for key,value in cue_details_for_graph.items()]
    cue_properties = [cue_details for cue_details in cue_details_for_graph.items()]

    # Create trace for D2D communication points

    trace_points_cue = go.Scatter(
        x=cue_x_values,
        y=cue_y_values,
        mode='markers',
        # marker=dict(color='red'),
        # marker=dict(color=[determine_color[(x, y)] for x, y in zip(cue_x_values, cue_y_values)]),
        marker=dict(symbol="triangle-up", size=10,color='red'),
        text=cue_properties,
        hoverinfo='text',
        name='CUE Points'
    )

    # Extract x and y coordinates for cue pairs 
    due_x_values = [due_details_for_graph[key]["tx"] for key,value in due_details_for_graph.items()]
    due_y_values = [due_details_for_graph[key]["ty"] for key,value in due_details_for_graph.items()]
    due_properties = [due_details for due_details in due_details_for_graph.items()]

    # Create trace for D2D communication points

    trace_points_due = go.Scatter(
        x=due_x_values,
        y=due_y_values,
        mode='markers',
        # marker=dict(color='red'),
        # marker=dict(color=[determine_color[(x, y)] for x, y in zip(due_x_values, due_y_values)]),
        marker=dict(color='blue',size=10),
        text=due_properties,
        hoverinfo='text',
        name='DUE Points'
    )
    
    circle_traces = []
    circle_radius = 40  # Radius in meters

    alt = False
    for x, y in zip(due_x_values, due_y_values):
        if(alt == True):
            alt = False
            continue;
        
        # Generate points for the circle centered at (x, y)
        theta_values = np.linspace(0, 2*np.pi, 360)  # Angle values from 0 to 2pi
        circle_x = x + circle_radius * np.cos(theta_values)
        circle_y = y + circle_radius * np.sin(theta_values)
        
        # Create trace for the circle centered at (x, y)
        circle_trace = go.Scatter(
            x=circle_x,
            y=circle_y,
            mode='lines',
            # ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
            line=dict(color='green', dash="dot"),
        )
        circle_traces.append(circle_trace)
        alt = True

    trace_point_mbs = go.Scatter(
        x=[0],
        y=[0],
        mode='markers',
        marker=dict(size=25,symbol="star",color='black'),
        name='Major Base Station'
    )

    # Create trace for circle
    circle_x = []
    circle_y = []
    for theta in range(361):
        circle_x.append(500 * np.cos(np.radians(theta)))
        circle_y.append(500 * np.sin(np.radians(theta)))

    trace_circle = go.Scatter(
        x=circle_x,
        y=circle_y,
        mode='lines',
        line=dict(color='black', dash='dash'),
        name='Circle'
    )

    # Create layout
    layout = go.Layout(
        title='D2D Communication Points with Circle',
        xaxis=dict(title='X Axis'),
        yaxis=dict(title='Y Axis'),
        hovermode='closest'
    )

    # Create figure
    fig = go.Figure(data=[trace_points_cue,trace_points_due,*circle_traces,trace_point_mbs, trace_circle], layout=layout)

    # Show plot
    fig.show()

    # # print(f'The total reward (reinfocement learning) : {cummulative_reward_value}')
    # print(f'initial value: {initial_cummulative_reward_value} and the final cummulative_reward_value {best_cummulative_reward_value}')


"""