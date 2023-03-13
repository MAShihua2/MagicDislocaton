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
        # points = map(lambda x:x.insert(fix_coord, s_center_pos[fix_coord]), points)
        for i, point in enumerate(points):
            point.insert(fix_coord, s_center_pos[fix_coord])
        return np.array(points)
    
    def rotate_S_plane(self, s_edge_points, s_center_pos, fix_coord, insert_plane, target_plane, cos_theta, margin_base, margin_scale, margin_flag, cross=False):
        rotation_matrix = get_rotation_info(insert_plane, target_plane, cos_theta)
        margin = margin_scale[0] / margin_scale[1] * np.sqrt(margin_base) * self.lattice * margin_flag

        for s_tri_point in s_edge_points:
            if cross and s_tri_point[fix_coord+1%3] < margin:
                s_tri_point[1] += margin
                continue
            s_tri_point[fix_coord] -= s_center_pos[fix_coord]
            trans_pos = np.dot(rotation_matrix, s_tri_point.reshape(-1, 1))
            trans_pos[fix_coord] += s_center_pos[fix_coord]
            s_tri_point[0:] = trans_pos.reshape(-1)
            s_tri_point[1] += margin
        return s_edge_points
    
    def show_points(self, s_edge_points, atom_points):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(s_edge_points[:, 0], s_edge_points[:, 1], s_edge_points[:, 2], label="s_points", s=2)
        ax.scatter(atom_points[::1000, 0], atom_points[::1000, 1], atom_points[::1000, 2], label="atom_points", s=1)
        # plt.show()
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        # plt.show()
        plt.savefig("test.jpg")

    
    def create_dislocation(self, move_step, move_direction, move_layer_range, s_para):
        move_direction = np.array(move_direction)
        b = move_step * self.lattice
        move_b = b * move_direction / np.linalg.norm(move_direction)

        if s_para["type"] == "rect":
            # determine the center plane
            s_center_pos = s_para['center_pos']
            dx, dy, dz = s_para["edge_range"]
            s_edge_points = self.get_rect_edge_points(s_center_pos, dx=dx, dy=dy, dz=dz)
            s_tri_points = self.define_S(s_center_pos, s_edge_points)
            s_shape = s_tri_points.shape
        elif s_para["type"] == "loop":
            s_center_pos = s_para['center_pos']
            fix_coord = s_para['fix_coord']
            num_points = s_para["num_points"]
            scale = s_para['scale']
            base = s_para['base']
            s_edge_points = self.get_loop_edge_points(s_center_pos, fix_coord, num_points, scale, base)
            
            if s_para["rotate_para"] is not None:
                rotate_para = s_para["rotate_para"]
                s_edge_points = self.rotate_S_plane(s_edge_points=s_edge_points, s_center_pos=s_center_pos,
                                                   fix_coord=fix_coord,
                                                   insert_plane=rotate_para['insert_plane'],
                                                   target_plane=rotate_para['target_plane'],
                                                   cos_theta=rotate_para['cos_theta'],
                                                   margin_base=rotate_para['margin_base'], 
                                                   margin_scale=rotate_para['margin_scale'],
                                                   margin_flag=rotate_para['margin_flag'],
                                                   cross=rotate_para['cross'])
                                                   
            s_tri_points = self.define_S(s_center_pos, s_edge_points)
            s_shape = s_tri_points.shape
        self.show_points(s_edge_points, self.data[:, 2:5])
        new_atom = []
        for i, item in enumerate(self.data):
            layer = self.layer_info[i]
            if self.layer_num / 2 - move_layer_range < layer < self.layer_num / 2 + move_layer_range:
                # n * 3 * 3
                di_vectors = s_tri_points[:, :, :] - item[2:5]
                di_vectors = di_vectors / np.sqrt((di_vectors * di_vectors).sum(2)).reshape(s_shape[0], 3, 1)
                u1 = di_vectors[:, 0, :]
                u2 = di_vectors[:, 1, :]
                u3 = di_vectors[:, 2, :]
                solid_angles = get_omega(u1, u2, u3)
                s = -sum(solid_angles)
                us = - s * move_b / (4 * np.pi)
                item[2] += us[0]
                item[3] += us[1]
                item[4] += us[2]
                new_atom.append(item)
            else:
                new_atom.append(item)
        print(f"{datetime.now()} =====> Has revised the atom positions")
        self.write(new_atom)