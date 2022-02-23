import csv
import torch
import numpy as np
from torch.utils.data import Dataset
import pdb

#将图数据处理成邻接矩阵
def get_adjacent_matrix(distance_file: str, num_nodes: int, id_file: str = None, graph_type="connect") -> np.array:
    """
    :param distance_file: str, path of csv file to save the distances between nodes.
    :param num_nodes: int, number of nodes in the graph
    :param id_file: str, path of txt file to save the order of the nodes.
    :param graph_type: str, ["connect", "distance"]
    :return:
        np.array(N, N)
    """
    A = np.zeros([int(num_nodes), int(num_nodes)]) #构造全0 的邻接矩阵

    if id_file: #给节点排序
        with open(id_file, "r") as f_id:
            node_id_dict = {int(node_id): idx for idx, node_id in enumerate(f_id.read().strip().split("\n"))}

            with open(distance_file, "r") as f_d:
                f_d.readline()
                reader = csv.reader(f_d)
                for item in reader:
                    if len(item) != 3:
                        continue
                    i, j, distance = int(item[0]), int(item[1]), float(item[2])
                    if graph_type == "connect": #构造不带权值的邻接矩阵
                        A[node_id_dict[i], node_id_dict[j]] = 1.
                        A[node_id_dict[j], node_id_dict[i]] = 1.
                    elif graph_type == "distance":#构造带权值的邻接矩阵，距离越长权值越小
                        A[node_id_dict[i], node_id_dict[j]] = 1. / distance
                        A[node_id_dict[j], node_id_dict[i]] = 1. / distance
                    else:
                        raise ValueError("graph type is not correct (connect or distance)")
        return A #返回邻接矩阵

    with open(distance_file, "r") as f_d:
        f_d.readline()# 跳过表头
        reader = csv.reader(f_d)#读取csv文件
        for item in reader:
            if len(item) != 3:#数据有误
                continue
            i, j, distance = int(item[0]), int(item[1]), float(item[2]) #出发点，进入点，边的距离

            if graph_type == "connect": #无权重
                A[i, j], A[j, i] = 1., 1.
            elif graph_type == "distance":#有权重
                A[i, j] = 1. / distance
                A[j, i] = 1. / distance
            else:
                raise ValueError("graph type is not correct (connect or distance)")

    return A


def get_flow_data(flow_file: str) -> np.array: #每个节点的特征矩阵
    """
    :param flow_file: str, path of .npz file to save the traffic flow data
    :return:
        np.array(N, T, D)
    """
    data = np.load(flow_file)
    # a = data['data']#取出数据
    # b = a.transpose([1, 0, 2]) #将列调换顺序
    # c = b[:, :, 0] #只取一个特质
    # d = c[:, :, np.newaxis] #增添一列方便后续数据处理

    flow_data = data['data'].transpose([1, 0, 2])[:, :, 0][:, :, np.newaxis]

    return flow_data


class LoadData(Dataset):# 这个就是把读入的数据处理成模型需要的训练数据和测试数据，一个一个样本能读取出来
    def __init__(self, data_path, num_nodes, divide_days, time_interval, history_length, train_mode):
        """
        :param data_path: list, ["graph file name" , "flow data file name"], path to save the data file names.
        :param num_nodes: int, number of nodes.
        :param divide_days: list, [ days of train data, days of test data], list to divide the original data.
        :param time_interval: int, time interval between two traffic data records (mins).
        :param history_length: int, length of history data to be used.
        :param train_mode: list, ["train", "test"].
        """

        self.data_path = data_path #文件路径
        self.num_nodes = num_nodes #节点数
        self.train_mode = train_mode #训练类型：train , test
        self.train_days = divide_days[0]  # 45 days of train data 前面多少天的数据参与训练
        self.test_days = divide_days[1]  # 14 days of test data 预测后面多少天的数据，测试的时候就是使用多少天数据进行预测
        self.history_length = history_length  # 6
        self.time_interval = time_interval  # 5 min 数据每隔多久记录一次

        self.one_day_length = int(24 * 60 / self.time_interval) #每天记录多少次数据

        self.graph = get_adjacent_matrix(distance_file=data_path[0], num_nodes=num_nodes) #返回图的邻接矩阵

        # self.flow_norm, self.flow_data = self.pre_process_data(data=get_flow_data(data_path[1]), norm_dim=1) #归一化处理后的数据
        data = get_flow_data(data_path[1])
        self.flow_norm, self.flow_data = self.pre_process_data(data, norm_dim=1) #归一化处理后的数据

    def __len__(self):
        """
        :return: length of dataset (number of samples).
        """
        if self.train_mode == "train":
            return self.train_days * self.one_day_length - self.history_length
        elif self.train_mode == "test":
            return self.test_days * self.one_day_length
        else:
            raise ValueError("train mode: [{}] is not defined".format(self.train_mode))

    def __getitem__(self, index):  # (x, y), index = [0, L1 - 1]
        """
        :param index: int, range between [0, length - 1].
        :return:
            graph: torch.tensor, [N, N].
            data_x: torch.tensor, [N, H, D].
            data_y: torch.tensor, [N, 1, D].
        """
        if self.train_mode == "train":
            index = index
        elif self.train_mode == "test":
            index += self.train_days * self.one_day_length
        else:
            raise ValueError("train mode: [{}] is not defined".format(self.train_mode))

        data_x, data_y = LoadData.slice_data(self.flow_data, self.history_length, index, self.train_mode)

        data_x = LoadData.to_tensor(data_x)  # [N, H, D]
        data_y = LoadData.to_tensor(data_y).unsqueeze(1)  # [N, 1, D]

        return {"graph": LoadData.to_tensor(self.graph), "flow_x": data_x, "flow_y": data_y}

    @staticmethod
    def slice_data(data, history_length, index, train_mode):
        """
        :param data: np.array, normalized traffic data.
        :param history_length: int, length of history data to be used.
        :param index: int, index on temporal axis.
        :param train_mode: str, ["train", "test"].
        :return:
            data_x: np.array, [N, H, D].
            data_y: np.array [N, D].
        """
        if train_mode == "train":
            start_index = index
            end_index = index + history_length
        elif train_mode == "test":
            start_index = index - history_length
            end_index = index
        else:
            raise ValueError("train model {} is not defined".format(train_mode))

        data_x = data[:, start_index: end_index]
        data_y = data[:, end_index]

        return data_x, data_y

    @staticmethod
    def pre_process_data(data, norm_dim):
        """
        :param data: np.array, original traffic data without normalization.
        :param norm_dim: int, normalization dimension. 归一化的维度，就是说在哪个维度上归一化,这里是在dim=1时间维度上
        :return:
            norm_base: list, [max_data, min_data], data of normalization base.
            norm_data: np.array, normalized traffic data.
        """
        norm_base = LoadData.normalize_base(data, norm_dim)  # find the normalize base
        norm_data = LoadData.normalize_data(norm_base[0], norm_base[1], data)  # normalize data

        return norm_base, norm_data

    @staticmethod
    def normalize_base(data, norm_dim):
        """
        :param data: np.array, original traffic data without normalization.
        :param norm_dim: int, normalization dimension.
        :return:
            max_data: np.array
            min_data: np.array
        """
        max_data = np.max(data, norm_dim, keepdims=True)  # [N, T, D] , norm_dim=1, [N, 1, D]
        min_data = np.min(data, norm_dim, keepdims=True)
        return max_data, min_data

    @staticmethod
    def normalize_data(max_data, min_data, data):
        """
        :param max_data: np.array, max data.
        :param min_data: np.array, min data.
        :param data: np.array, original traffic data without normalization.
        :return:
            np.array, normalized traffic data.
        """
        mid = min_data
        base = max_data - min_data
        normalized_data = (data - mid) / base

        return normalized_data

    @staticmethod
    def recover_data(max_data, min_data, data):
        """
        :param max_data: np.array, max data.
        :param min_data: np.array, min data.
        :param data: np.array, normalized data.
        :return:
            recovered_data: np.array, recovered data.
        """
        mid = min_data
        base = max_data - min_data

        recovered_data = data * base + mid

        return recovered_data

    @staticmethod
    def to_tensor(data):
        return torch.tensor(data, dtype=torch.float)


if __name__ == '__main__':
    train_data = LoadData(data_path=["PeMS_04/PeMS04.csv", "PeMS_04/PeMS04.npz"], num_nodes=307, divide_days=[45, 14],
                          time_interval=5, history_length=6,
                          train_mode="train")

    print(len(train_data))
    print(train_data[0]["flow_x"].size())
    print(train_data[0]["flow_y"].size())
