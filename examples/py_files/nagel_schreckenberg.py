#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Import necessary modules

import numpy as np
from matplotlib import pyplot as plt


#%% Set the parameters of the problem

# Parameters of the simulation
T = 1000

# Parameters of the model
M = 1500
N = 350
v_max = 5
p = 0.3

# Create vectors with placeholder content (pre-allocation)
road = np.zeros(M, dtype=int)
speeds = np.zeros(M, dtype=int)
history_road = np.zeros((T, M), dtype=int)
history_speeds = np.zeros((T, M), dtype=int)


#%% Definition of useful functions

def adjust_speed(current_speed, next_driver_distance, speed_limit, prob_slowdown):
    v_bar = np.min([current_speed + 1, speed_limit])
    v_hat = np.min([v_bar, next_driver_distance - 1])
    uniform_random_number = np.random.uniform()  # from U([0, 1])
    if uniform_random_number < prob_slowdown:
        v = np.max([0, v_hat - 1])
    else:
        v = v_hat
    new_speed = v
    return new_speed


def period_transition(current_road, current_speeds, speed_limit, prob_slowdown):
    M = current_road.size
    drivers_locations = np.where(current_road == 1)[0]
    new_road = np.zeros_like(current_road, dtype=int)
    new_speeds = np.zeros_like(current_speeds, dtype=int)
    for l in drivers_locations:
        if l != drivers_locations[-1]:
            space_ahead = road[l+1] - road[l]
        else:  # hitting an edge case
            space_ahead = M - road[l] + road[drivers_locations[0]]
        new_speeds[l] = adjust_speed(current_speeds[l], space_ahead,
                                     speed_limit, prob_slowdown)
    for l in drivers_locations:
        if new_speeds[l] <= (M-1) - l:
            new_road[l + new_speeds[l]] = 1
        else:  # hitting an edge case
            new_road[new_speeds[l] - (M-1) + l] = 1
    return (new_road, new_speeds)


#%% Simulate the model

# Set the initial condition
initial_drivers_distance = M // N
for j in range(M):
    if j % initial_drivers_distance == 0:
        road[j] = 1
history_road[0, :] = road
history_speeds[0, :] = speeds

# Run the Monte-Carlo loop
for t in range(T):
    # Save current states to histories, for track records
    history_road[t, :] = road
    history_speeds[t, :] = speeds
    # Compute the policy functions, i.e., new road state and speeds
    new_road, new_speeds = period_transition(road, speeds, v_max, p)
    # Update the model conditions for next period
    road[:] = new_road
    speeds[:] = new_speeds


#%% Plot some results

plt.imshow(history_road, aspect='equal')
plt.tight_layout()


#%% Plot animated line

# from matplotlib import animation

# fig, ax = plt.subplots()
# scatter = ax.scatter([], [])

# def anim_init():
#     scatter.set_array([])

# def animate(i):
#     x = history_road[i, :]
#     y = np.zeros_like(road)
#     xy = np.block([x.reshape((-1, 1)), y.reshape((-1, 1))])
#     scatter.set_array(xy)
#     return scatter

# anim = animation.FuncAnimation(fig, animate, init_func=anim_init, frames=T, interval=100)
