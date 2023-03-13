"""
This file aims to create <110> dislocation for gaitaikuang with two layers deleted
class-based method
This file could move atoms according to a given S_plane
"""
import os
import tqdm
from datetime import datetime
import numpy as np
from utils import get_omega


class DislocationCreatorBase(object):

    def __init__(self, data_config, layerization_config) -> None:
        head, data, tail = self.read_data(data_config['input_file'], data_config['data_line_item_num'], read_type=data_config['type'])
        self.head = head
        self.tail = tail
        self.data = np.array(data)
        self.lattice = data_config['lattice']
        self.dxdydz = data_config['dxdydz']
        # read data
        self.output_file = data_config['input_file'].replace("dat", "moved.dat")
        # layerzie
        layerize_direction = layerization_config['direction']
        pos_index = data_config['pos_index']
        dxdydz = [0, 0, 0]
        dxdydz[layerize_direction] = self.dxdydz[layerize_direction]
        self.layer_info = self.layerize(self.data[:, pos_index[0]:pos_index[1]], self.lattice, dx=dxdydz[0], dy=dxdydz[1], dz=dxdydz[2])
        self.layer_num = len(set(self.layer_info))
        print(f"{datetime.now()} =====> Has layerized the data !")
        self.get_data_info()
        print(f"{datetime.now()} =====> Has obtain the data information !")
        print(f"{datetime.now()} =====> Has initilized the DislocationCreator !")
        # create dislocation
        # self.create_dislocation(self.center_pos, self.step)

    def read_data(self, input_file, data_line_item_num, read_type=None):
        lines = open(input_file, "r").readlines()
        head_lines = []
        data_lines = []
        tail_lines = []
        read_head = True
        read_data = False
        read_tail = False
        for line in lines:
            items = line.strip().split() 
            if len(items) != data_line_item_num:
                if read_head:
                    head_lines += [line]
                else:
                    read_tail = True
                    tail_lines += [line]
            else:
                if read_head:
                    read_head = False
                    read_data = True
                if read_data and not read_head and not read_tail:
                    data_lines.append([eval(v) for v in items])
        print(f"{datetime.now()} =====> Read {len(data_lines)} Atoms")
        return head_lines, data_lines, tail_lines

        
    
    def get_data_info(self):
        data = self.data
        self.num = len(data)
        self.x_range = (min(data[:, 3]), max(data[:, 3]))
        self.y_range = (min(data[:, 4]), max(data[:, 4]))
        self.z_range = (min(data[:, 5]), max(data[:, 5]))
        self.x_len = self.x_range[1] - self.x_range[0]
        self.y_len = self.y_range[1] - self.y_range[0]
        self.z_len = self.z_range[1] - self.z_range[0]


        print(f"{datetime.now()} =====> Range of X-axis: ", self.x_range)
        print(f"{datetime.now()} =====> Range of Y-axis: ", self.y_range)
        print(f"{datetime.now()} =====> Range of Z-axis: ", self.z_range)

    def layerize(self, data, a, dx=0, dy=0, dz=0):
        """
        layerize data with a axis
        data: list of (x, y, z)
        a: lattice
        dx: coefficiency
        layer length = dx/dy/dz * a
        """
        d = a * max(dx, dy, dz)
        pos_index = np.argmax([dx, dy, dz])
        
        min_pos = min(data[:, pos_index])
        max_pos = max(data[:, pos_index])
        layer_ranges = [(min_pos - d / 2, min_pos + d / 2)]

        while True:
            last_range = layer_ranges[-1] #最下层的原子面range给last_range,last_range即为下一层面的range[左边界，右边界】
            new_range = (last_range[1], last_range[1] + d) #[1]右边界，new_range+dy进行更新
            layer_ranges.append(new_range) #产生一个y_range的列表
            if last_range[1] + d >= max_pos:
                break

        num_plane = len(layer_ranges)
        print(f"{datetime.now()} =====> Number of Layers", num_plane)
        print(f"{datetime.now()} =====> First layer: ", layer_ranges[0])
        print(f"{datetime.now()} =====> Last layer: ", layer_ranges[-1])

        layer_info = []
        for item in data:
            atom_pos = item[pos_index]
            for i, layer_range in enumerate(layer_ranges):
                if layer_range[0] <= atom_pos <= layer_range[1]:
                    layer_info += [i]
                    break
        return layer_info


    def write(self, data):
        f = open(self.output_file, "w")
        f.writelines(self.head)
        for item in tqdm.tqdm(data):
            line = " ".join([str(v) if i not in [0, 1] else str(int(v)) for i, v in enumerate(item)]) + '\n'
            f.write(line)

    def define_S(self, s_center, edge_points):
        """
        s_center: the center point of S
        r: the distance of each point of S plane from the center point
        """
        s_tri_points = [[s_center, edge_points[i], edge_points[(i+1)%len(edge_points)]] for i in range(len(edge_points))]
        return np.array(s_tri_points)

    def get_rect_edge_points(self, center_pos, dx=0, dy=0, dz=0):
        center_pos = np.array(center_pos)
        dxyz = np.array([dx, dy, dz])
        if dz == 0:
            operator_list = [[-1, 1, 0], [1, 1, 0], [1, -1, 0], [-1, -1, 0]]
        elif dy == 0:
            operator_list = [[-1, 0, 1], [1, 0, 1], [1, 0, -1], [-1, 0, -1]]
        elif dx == 0:
            operator_list = [[0, -1, 1], [0, 1, 1], [0, 1, -1], [0, -1, -1]]

        return [center_pos + np.array(oper) * dxyz for oper in operator_list]


    def create_dislocation(self, move_step, move_direction, move_layer_range, s_para):
        move_direction = np.array(move_direction)
        b = move_step * self.lattice
        move_b = b * move_direction / np.linalg.norm(move_direction)

        if s_para["type"] == "rect":
            # determine the center plane
            dx, dy, dz = s_para["edge_range"]
            s_center_pos = s_para['center_pos']
            s_edge_points = self.get_rect_edge_points(s_center_pos, dx=dx, dy=dy, dz=dz)
            s_tri_points = self.define_S(s_center_pos, s_edge_points)
            s_shape = s_tri_points.shape

        new_atom = []
        for i, item in enumerate(self.data):
            layer = self.layer_info[i]
            if self.layer_num / 2 - move_layer_range < layer < self.layer_num / 2 + move_layer_range :
                # n * 3 * 3
                di_vectors = s_tri_points[:, :, :] - item[3:6]
                di_vectors = di_vectors / np.sqrt((di_vectors * di_vectors).sum(2)).reshape(s_shape[0], 3, 1)
                u1 = di_vectors[:, 0, :]
                u2 = di_vectors[:, 1, :]
                u3 = di_vectors[:, 2, :]
                solid_angles = get_omega(u1, u2, u3)
                s = -sum(solid_angles)
                us = - s * move_b / (4 * np.pi)
                item[3] += us[0]
                item[4] += us[1]
                item[5] += us[2]
                new_atom.append(item)
            else:
                new_atom.append(item)
        print(f"{datetime.now()} =====> Has revised the atom positions")
        self.write(new_atom)
 

