import math

import numpy as np
import networkx as nx
import pandas as pd
from EdgeNode import EdgeNode
from EndDevice import EndDevice

class FLEnvironment:
    def __init__(self, network_node_path, network_edge_path, device_path, node_path, schedule_path):
        self.network_node_path = network_node_path
        self.network_edge_path = network_edge_path
        self.node_path = node_path
        self.device_path = device_path
        self.schedule_path = schedule_path
        self._build_network()

    def _build_network(self):
        cecGraph = nx.Graph()
        # build the FL architecture
        f1 = open(self.network_node_path, 'r')
        lines = f1.readlines()
        for line in lines:
            line = line.replace('\n', '').replace('\r', '')
            info = line.split(',')
            if len(info) == 3:
                cecGraph.add_node(int(info[0]), name=info[1], weight=info[2])
        f1.close()

        f2 = open(self.network_edge_path, 'r')
        lines = f2.readlines()
        for line in lines:
            line = line.replace('\n', '').replace('\r', '')
            info = line.split(',')
            if len(info) == 3:
                cecGraph.add_edge(int(info[0]), int(info[1]), weight=float(info[2]))
                cecGraph[int(info[0])][int(info[1])]['flow'] = []
        f2.close()

        deviceList = []
        f1 = open(self.device_path, 'r')
        lines = f1.readlines()
        for line in lines:
            line = line.replace('\n', '').replace('\r', '')
            info = line.split(',')
            if len(info) == 4:
                device = EndDevice(int(info[0]), int(info[1]), float(info[2]), int(info[3]))
                # device.printInfo()
                deviceList.append(device)
        f1.close()

        nodeList = []
        f1 = open(self.node_path, 'r')
        lines = f1.readlines()
        for line in lines:
            line = line.replace('\n', '').replace('\r', '')
            info = line.split(',')
            if len(info) == 1:
                node = EdgeNode(int(info[0]))
                # device.printInfo()
                nodeList.append(node)
        f1.close()
        now_schedule = pd.read_csv(self.schedule_path)
        self.cecGraph = cecGraph
        self.deviceList = deviceList
        self.nodeList = nodeList
        self.state_df = now_schedule
        self.state = self.state_df.iloc[0]

    def reset(self):
        return self.state

    def step(self, action, time_step):
        # TODO 保证action产生的元素是列表
        #  假设所有client的策略一致
        theta_rate = 0.4 + abs(action[0]) - int(abs(action[0])* 10)/10
        theta_rate_list = [1,1,1,1,1]
        B_rate_list = [0,0,0,0,0]
        B_rate = 0.4 + abs(action[0]) - int(abs(action[0])* 10)/10
        sublist = [0.1,0.2,0.3,0.4]
        B_sum = 0
        theta_sum = 0
        for i in range(4):
            B_rate_list[i] = B_rate - sublist[i]
            theta_rate_list[i] = theta_rate - sublist[i]
            B_sum = B_sum + B_rate_list[i]
            theta_sum = theta_sum + theta_rate_list[i]
        B_rate_list[4] = 1 - B_sum
        theta_rate_list[4] = 1 - theta_sum
        cloud_finish_time = 0
        for j in range(len(self.deviceList)):
            # TODO revise
            ctime = self.deviceList[j].dataset / (self.deviceList[j].cpuNum * theta_rate)
            edge_0 = self.deviceList[j].uploadNode
            edge_1 = self.deviceList[j].deviceId
            edge_name = "edge_weight_"+str(edge_0)+str(edge_1)
            cloud_finish_time = max(cloud_finish_time, cloud_finish_time+ctime)
            begin_t = time_step
            # TODO update state(local training)
            for i in range(begin_t, begin_t + int(ctime) + 1):
                if i in self.state_df['time'].values.tolist():
                    self.state_df.loc[self.state_df['time'] == i, edge_name] = \
                        self.state_df.loc[self.state_df['time'] == i, edge_name] + begin_t+int(ctime) - i
                else:
                    a = self.state_df.iloc[0].values.tolist()
                    d = pd.DataFrame(columns=self.state_df.columns)
                    d.loc[-1] = a
                    d['time'] = i
                    d[edge_name] =  begin_t+int(ctime) - i
                    self.state_df = pd.concat([d, self.state_df], axis=0, ignore_index=True)
        # # TODO update state(Edge transmission)
        # for i in range(begin_ptime, begin_ptime + int(ptime)+1):
        #     if i in self.state_df['time'].values.tolist():
        #         device_name = "device_"+str(target_action_device.deviceId)+"_time"
        #         self.state_df.loc[self.state_df['time'] == i, device_name] = self.state_df.loc[self.state_df['time'] == i, device_name] + begin_ptime + int(ptime)+1-i
        #
        # # TODO update state(Cloud transmission)
        # for i in range(begin_ptime, begin_ptime + int(ptime)+1):
        #     if i in self.state_df['time'].values.tolist():
        #         device_name = "device_"+str(target_action_device.deviceId)+"_time"
        #         self.state_df.loc[self.state_df['time'] == i, device_name] = self.state_df.loc[self.state_df['time'] == i, device_name] + begin_ptime + int(ptime)+1-i
        #
        #
        # # TODO 计算第1个edge node完成aggregation的时间，放在edge_completion_list中
        # edge_completion_list = {}
        # cluster_index = [4, 6, 9, 11, 13]
        # cluster = [[], [], [], [], []]
        # edge_completion_time1 = 0
        # for i in range(4):
        #     cluster[0].append(self.deviceList[i])
        #     ptime = self.deviceList[i].dataset / self.deviceList[i].cpuNum
        #     ctime = 0
        #     edge_completion_time1 = max(edge_completion_time1, ctime + ptime)
        # edge_completion_list[9] = edge_completion_time1
        # edge_completion_time2 = 0
        # for i in range(4,6):
        #     cluster[1].append(self.deviceList[i])
        #     ptime = self.deviceList[i].dataset / self.deviceList[i].cpuNum
        #     ctime = 0
        #     edge_completion_time2 = max(edge_completion_time2, ctime + ptime)
        # edge_completion_list[10] = edge_completion_time1
        # edge_completion_time3 = 0
        # for i in range(6,9):
        #     cluster[2].append(self.deviceList[i])
        #     ptime = self.deviceList[i].dataset / self.deviceList[i].cpuNum
        #     ctime = 0
        #     edge_completion_time3 = max(edge_completion_time3, ctime + ptime)
        # edge_completion_list[11] = edge_completion_time1
        # edge_completion_time4 = 0
        # for i in range(9,11):
        #     cluster[3].append(self.deviceList[i])
        #     ptime = self.deviceList[i].dataset / self.deviceList[i].cpuNum
        #     ctime = 0
        #     edge_completion_time4 = max(edge_completion_time4, ctime + ptime)
        # edge_completion_list[12] = edge_completion_time1
        # edge_completion_time5 = 0
        # for i in range(11,13):
        #     cluster[4].append(self.deviceList[i])
        #     ptime = self.deviceList[i].dataset / self.deviceList[i].cpuNum
        #     ctime = 0
        #     edge_completion_time5 = max(edge_completion_time5, ctime + ptime)
        #
        # edge_finish_time = time_step
        # for id, tval in edge_completion_list.items():
        #     edge_finish_time = max(edge_finish_time, tval+time_step)
        # # TODO 聚合后的model size来源于数据集 edge_model_info.csv
        # edge_model_size = [12,34,11,87,92]
        # cloud_completion_list = {}
        # index = 0
        # for id in edge_completion_list.keys():
        #     cloud_finish_time = edge_completion_list[id]
        #     cloud_finish_time = cloud_finish_time + edge_model_size[index] * theta_rate_list[index] / B_rate_list[index]
        #     cloud_completion_list[id] = cloud_finish_time
        #     index = index + 1
        # cloud_finish_time = 0
        # for id, tval in cloud_completion_list.items():
        #     cloud_finish_time = max(cloud_finish_time, tval+time_step)

        # up_bandwidth = []
        # cpu_cycles = []
        # down_bandwidth = []
        # finish_time = 0
        # for x in range(0, self.user_num):
        #     up_bandwidth.append(action[0])
        #     cpu_cycles.append(action[1])
        #     down_bandwidth.append(action[2])
        #
        # # TODO Revise
        # model_size = list(range(1, self.user_num+1))
        # data_size = list(range(1, self.user_num+1))
        # model_load = list(range(1, self.user_num+1))
        # # select the minimum of users
        # for i in range(self.user_num):
        #     compressed_size = self.compression_algo(data_size[i])
        #     upload_time = compressed_size / up_bandwidth[i]
        #     computation_time = model_load[i] / cpu_cycles[i]
        #     down_time = model_size[i] / down_bandwidth[i]
        #     finish_time = upload_time + computation_time + down_time
        # TODO 计算reward的公式
        self.reward = math.exp(-cloud_finish_time / 10)
        self.state_df.to_csv("now_schedule.csv", index=0)
        done = True
        return self.state, self.reward, done, cloud_finish_time

    def compression_algo(data_size):
        compressed_size = data_size / 2.0
        return compressed_size