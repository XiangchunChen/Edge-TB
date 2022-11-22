import os
import random

import pandas as pd

from ddpg_algo import DDPG

if __name__ == '__main__':

    s_dim = 20 # refer to now_schedule
    a_dim = 2 # <bandwidth, rate>
    a_bound = 2
    observation = pd.read_csv("now_schedule.csv").iloc[0]
    agent = DDPG(a_dim, s_dim, a_bound)
    agent.restore_net()
    action = agent.choose_action(observation)
    print(action)