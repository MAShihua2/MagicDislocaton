<<<<<<< HEAD
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from datetime import datetime
from utils import get_rotation_info, get_omega
from dislocation_creator_base import DislocationCreatorBase


class DislocationCreatorWithSplaneOperator(DislocationCreatorBase):

    def __init__(self, data_config, layerization_config) -> None:
        super(DislocationCreatorWithSplaneOperator, self).__init__(data_config, layerization_config)

    def get_loop_edge_points(self, s_center_pos, fix_coord, num_points, scale, base):
        S_R = scale * np.sqrt(base) * self.lattice
        theta_list = list(np.linspace(0, 2 * np.pi, num_points+1))
        points = [[S_R * np.cos(theta) if abs(S_R * np.cos(theta)) > 1e-8 else 0,
                   S_R * np.sin(theta) if abs(S_R * np.sin(theta)) > 1e-8 else 0
                  ] for theta in theta_list]
        
        for i, point in enumerate(points):
            point.insert(fix_coord, 0)
            point[0] += s_center_pos[0]
            point[1] += s_center_pos[1]
            point[2] += s_center_pos[2]
        return np.array(points)
    
    def get_insert_edge_points(self, edge_points, insert_index, extra_points):
        new_edge_points = []
        for i, item in enumerate(edge_points):
            new_edge_points.append(list(item))
            if i == insert_index:
                new_edge_points += extra_points
        return np.array(new_edge_points)
    
    def get_sin_points(self, A, omega, num_points, start_point, end_point, s_center_pos, fix_coord):
        theta_list = list(np.linspace(np.pi / 4, 2 * np.pi + np.pi / 4, num_points))
        delta_index = np.argmax(abs(end_point - start_point))
        delta_values = list(np.linspace(start_point[delta_index], end_point[delta_index], num_points))
        sin_values = [A * np.sin(omega * theta) for theta in theta_list]

        points = []
        for i in range(num_points):
            tmp_pos = [0, 0, 0]
            tmp_pos[delta_index] = delta_values[i]
            tmp_pos[fix_coord] = s_center_pos[fix_coord]
            res_index = [0, 1, 2]
            res_index.remove(delta_index)
            res_index.remove(fix_coord)
            res_index = res_index[0]
            tmp_pos[res_index] = sin_values[i]
            points.append(tmp_pos)

        return points

    def rotate_S_plane(self, s_edge_points, s_center_pos, fix_coord, insert_plane, target_plane):
        rotation_matrix = get_rotation_info(insert_plane, target_plane)
        # margin = margin_scale[0] / margin_scale[1] * np.sqrt(margin_base) * self.lattice * margin_flag

        for s_tri_point in s_edge_points:
            # if cross and s_tri_point[fix_coord+1%3] < margin:
                # s_tri_point[1] += margin
                # continue
            s_tri_point[fix_coord] -= s_center_pos[fix_coord]
            trans_pos = np.dot(rotation_matrix, s_tri_point.reshape(-1, 1))
            trans_pos[fix_coord] += s_center_pos[fix_coord]
            s_tri_point[0:] = trans_pos.reshape(-1)
            # s_tri_point[1] += margin
        return s_edge_points
    
    def show_points(self, s_edge_points, atom_points):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot(s_edge_points[:, 0], s_edge_points[:, 1], zs=s_edge_points[:, 2], label="s_points")
        ax.scatter(atom_points[::1000, 0], atom_points[::1000, 1], atom_points[::1000, 2], label="atom_points", s=1)
        # plt.show()
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()
        plt.savefig("test.jpg")

    
    def create_dislocation(self, move_step, move_direction, move_layer_range, s_para):
        move_direction = np.array(move_direction)
        b = move_step * self.lattice
        move_b = b * move_direction / np.linalg.norm(move_direction)
        print(s_para["center_pos"])
        if s_para["type"] == "rect" or s_para["type"] == "sin" or s_para["type"] == "line":
            # determine the center plane
            s_center_pos = s_para['center_pos']
            dx, dy, dz = s_para["edge_range"]
            s_edge_points = self.get_rect_edge_points(s_center_pos, dx=dx, dy=dy, dz=dz)
            s_edge_points = np.array(s_edge_points)
            if s_para["type"] == "sin":
                sin_points = self.get_sin_points(s_para["sin"]["A"], 
                                                 s_para["sin"]["omega"], 
                                                 s_para["sin"]["num_points"],
                                                 start_point=s_edge_points[s_para["sin"]["start"]],
                                                 end_point=s_edge_points[s_para["sin"]["end"]],
                                                 s_center_pos=s_center_pos,
                                                 fix_coord=s_para["sin"]["fix_coord"])
                
                s_edge_points = self.get_insert_edge_points(s_edge_points, insert_index=s_para["sin"]["start"], extra_points=sin_points)
            s_tri_points = self.define_S(s_center_pos, s_edge_points)
            s_shape = s_tri_points.shape
        elif s_para["type"] == "loop":
            s_center_pos = s_para['center_pos']
            fix_coord = s_para['fix_coord']
            num_points = s_para["num_points"]
            scale = s_para['scale']
            base = s_para['base']
            s_edge_points = self.get_loop_edge_points(s_center_pos, fix_coord, num_points, scale, base)
            print(s_para)
            if s_para["rotate_para"] is not None:
                rotate_para = s_para["rotate_para"]
                print("rotate!")
                s_edge_points = self.rotate_S_plane(s_edge_points=s_edge_points, s_center_pos=s_center_pos,
                                                   fix_coord=fix_coord,
                                                   insert_plane=rotate_para['insert_plane'],
                                                   target_plane=rotate_para['target_plane'],)
                                                   
            s_tri_points = self.define_S(s_center_pos, s_edge_points)
            s_shape = s_tri_points.shape
        self.show_points(s_edge_points, self.data[:, 2:5])
        new_atom = []
        for i, item in enumerate(self.data):
            layer = self.layer_info[i]
            if self.get_layer(s_center_pos, self.layerize_direction) - move_layer_range < layer < self.get_layer(s_center_pos, self.layerize_direction) + move_layer_range:
                # n * 3 * 3
                di_vectors = s_tri_points[:, :, :] - item[2:5]
                di_vectors = di_vectors / np.sqrt((di_vectors * di_vectors).sum(2)).reshape(s_shape[0], 3, 1)
                u1 = di_vectors[:, 0, :]
                u2 = di_vectors[:, 1, :]
                u3 = di_vectors[:, 2, :]
                solid_angles = get_omega(u1, u2, u3)
                s = -sum(solid_angles)
                # s = sum(solid_angles)
                us = - s * move_b / (4 * np.pi)
                item[2] += us[0]
                item[3] += us[1]
                item[4] += us[2]
                new_atom.append(item)
            else:
                new_atom.append(item)
        print(f"{datetime.now()} =====> Has revised the atom positions")
=======
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from datetime import datetime
from utils import get_rotation_info, get_omega
from dislocation_creator_base import DislocationCreatorBase


class DislocationCreatorWithSplaneOperator(DislocationCreatorBase):

    def __init__(self, data_config, layerization_config) -> None:
        super(DislocationCreatorWithSplaneOperator, self).__init__(data_config, layerization_config)

    def get_loop_edge_points(self, s_center_pos, fix_coord, num_points, scale, base):
        S_R = scale * np.sqrt(base) * self.lattice
        theta_list = list(np.linspace(0, 2 * np.pi, num_points+1))
        points = [[S_R * np.cos(theta) if abs(S_R * np.cos(theta)) > 1e-8 else 0,
                   S_R * np.sin(theta) if abs(S_R * np.sin(theta)) > 1e-8 else 0
                  ] for theta in theta_list]
        
        for i, point in enumerate(points):
            point.insert(fix_coord, 0)
            point[0] += s_center_pos[0]
            point[1] += s_center_pos[1]
            point[2] += s_center_pos[2]
        return np.array(points)
    
    def get_insert_edge_points(self, edge_points, insert_index, extra_points):
        new_edge_points = []
        for i, item in enumerate(edge_points):
            new_edge_points.append(list(item))
            if i == insert_index:
                new_edge_points += extra_points
        return np.array(new_edge_points)
    
    def get_sin_points(self, A, omega, num_points, start_point, end_point, s_center_pos, fix_coord):
        theta_list = list(np.linspace(np.pi / 4, 2 * np.pi + np.pi / 4, num_points))
        delta_index = np.argmax(abs(end_point - start_point))
        delta_values = list(np.linspace(start_point[delta_index], end_point[delta_index], num_points))
        sin_values = [A * np.sin(omega * theta) for theta in theta_list]

        points = []
        for i in range(num_points):
            tmp_pos = [0, 0, 0]
            tmp_pos[delta_index] = delta_values[i]
            tmp_pos[fix_coord] = s_center_pos[fix_coord]
            res_index = [0, 1, 2]
            res_index.remove(delta_index)
            res_index.remove(fix_coord)
            res_index = res_index[0]
            tmp_pos[res_index] = sin_values[i]
            points.append(tmp_pos)

        return points

    def rotate_S_plane(self, s_edge_points, s_center_pos, fix_coord, insert_plane, target_plane):
        rotation_matrix = get_rotation_info(insert_plane, target_plane)
        # margin = margin_scale[0] / margin_scale[1] * np.sqrt(margin_base) * self.lattice * margin_flag

        for s_tri_point in s_edge_points:
            # if cross and s_tri_point[fix_coord+1%3] < margin:
                # s_tri_point[1] += margin
                # continue
            s_tri_point[fix_coord] -= s_center_pos[fix_coord]
            trans_pos = np.dot(rotation_matrix, s_tri_point.reshape(-1, 1))
            trans_pos[fix_coord] += s_center_pos[fix_coord]
            s_tri_point[0:] = trans_pos.reshape(-1)
            # s_tri_point[1] += margin
        return s_edge_points
    
    def show_points(self, s_edge_points, atom_points):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot(s_edge_points[:, 0], s_edge_points[:, 1], zs=s_edge_points[:, 2], label="s_points")
        ax.scatter(atom_points[::1000, 0], atom_points[::1000, 1], atom_points[::1000, 2], label="atom_points", s=1)
        # plt.show()
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()
        plt.savefig("test.jpg")

    
    def create_dislocation(self, move_step, move_direction, move_layer_range, s_para):
        move_direction = np.array(move_direction)
        b = move_step * self.lattice
        move_b = b * move_direction / np.linalg.norm(move_direction)
        print(s_para["center_pos"])
        if s_para["type"] == "rect" or s_para["type"] == "sin" or s_para["type"] == "line":
            # determine the center plane
            s_center_pos = s_para['center_pos']
            dx, dy, dz = s_para["edge_range"]
            s_edge_points = self.get_rect_edge_points(s_center_pos, dx=dx, dy=dy, dz=dz)
            s_edge_points = np.array(s_edge_points)
            if s_para["type"] == "sin":
                sin_points = self.get_sin_points(s_para["sin"]["A"], 
                                                 s_para["sin"]["omega"], 
                                                 s_para["sin"]["num_points"],
                                                 start_point=s_edge_points[s_para["sin"]["start"]],
                                                 end_point=s_edge_points[s_para["sin"]["end"]],
                                                 s_center_pos=s_center_pos,
                                                 fix_coord=s_para["sin"]["fix_coord"])
                
                s_edge_points = self.get_insert_edge_points(s_edge_points, insert_index=s_para["sin"]["start"], extra_points=sin_points)
            s_tri_points = self.define_S(s_center_pos, s_edge_points)
            s_shape = s_tri_points.shape
        elif s_para["type"] == "loop":
            s_center_pos = s_para['center_pos']
            fix_coord = s_para['fix_coord']
            num_points = s_para["num_points"]
            scale = s_para['scale']
            base = s_para['base']
            s_edge_points = self.get_loop_edge_points(s_center_pos, fix_coord, num_points, scale, base)
            print(s_para)
            if s_para["rotate_para"] is not None:
                rotate_para = s_para["rotate_para"]
                print("rotate!")
                s_edge_points = self.rotate_S_plane(s_edge_points=s_edge_points, s_center_pos=s_center_pos,
                                                   fix_coord=fix_coord,
                                                   insert_plane=rotate_para['insert_plane'],
                                                   target_plane=rotate_para['target_plane'],)
                                                   
            s_tri_points = self.define_S(s_center_pos, s_edge_points)
            s_shape = s_tri_points.shape
        self.show_points(s_edge_points, self.data[:, 2:5])
        new_atom = []
        for i, item in enumerate(self.data):
            layer = self.layer_info[i]
            if self.get_layer(s_center_pos, self.layerize_direction) - move_layer_range < layer < self.get_layer(s_center_pos, self.layerize_direction) + move_layer_range:
                # n * 3 * 3
                di_vectors = s_tri_points[:, :, :] - item[2:5]
                di_vectors = di_vectors / np.sqrt((di_vectors * di_vectors).sum(2)).reshape(s_shape[0], 3, 1)
                u1 = di_vectors[:, 0, :]
                u2 = di_vectors[:, 1, :]
                u3 = di_vectors[:, 2, :]
                solid_angles = get_omega(u1, u2, u3)
                s = -sum(solid_angles)
                # s = sum(solid_angles)
                us = - s * move_b / (4 * np.pi)
                item[2] += us[0]
                item[3] += us[1]
                item[4] += us[2]
                new_atom.append(item)
            else:
                new_atom.append(item)
        print(f"{datetime.now()} =====> Has revised the atom positions")
>>>>>>> de2d02f6b59fc072d8386febfd84b80e1f0d12aa
        self.write(new_atom)