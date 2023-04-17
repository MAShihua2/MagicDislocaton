from ctypes import util
import enum
from numpy import ndarray
from tqdm import tqdm, trange
import numpy as np
from utils import get_omega, read_data,  get_rotation_info, define_plane_
import time
import os

# bcc
def move_v1(path, lattice, x_direct, y_direct, z_direct, burgers_vector, layerize_direct, target_plane, insert_plane, scale, base, num_points):  ###1/3[111] lie in {112}

    if (abs(x_direct[0]) + abs(x_direct[1]) + abs(x_direct[2])) % 2 == 0:
        dx = 1 / np.sqrt(np.power(x_direct,2).sum())
    else:
        dx = 1 / np.sqrt(np.power(x_direct,2).sum())
        dx = dx / 2
    if (abs(y_direct[0]) + abs(y_direct[1]) + abs(y_direct[2])) % 2 == 0:
        dy = 1 / np.sqrt(np.power(y_direct, 2).sum())
    else:
        dy = 1 / np.sqrt(np.power(y_direct, 2).sum())
        dy = dy / 2
    if (abs(z_direct[0]) + abs(z_direct[1]) + abs(z_direct[2])) % 2 == 0:
        dz = 1 / np.sqrt(np.power(z_direct, 2).sum())
    else:
        dz = 1 / np.sqrt(np.power(z_direct, 2).sum())
        dz = dz / 2
    dx = dx * lattice
    dy = dy * lattice
    dz = dz * lattice

    data, head_lines, tail_lines = read_data(path)

    move_step = np.sqrt(burgers_vector[0] ** 2 + burgers_vector[1] ** 2 + burgers_vector[2] ** 2)

    A_matrix = np.array([[x_direct[0], y_direct[0], z_direct[0]],
                         [x_direct[1], y_direct[1], z_direct[1]],
                         [x_direct[2], y_direct[2], z_direct[2]]])
    move_direction = np.linalg.solve(A_matrix, burgers_vector)
    move_direction = move_direction / np.sqrt(np.power(move_direction, 2).sum())

    move_b = move_step * move_direction * lattice

    S_R = scale* np.sqrt(base) * lattice
    
    # obtain center three layers of atoms in the system and define the plane
    A, B, C, pos_A, pos_B, pos_C, new_data = define_plane_(data, layerize_direct)
    if pos_A > pos_B and pos_A > pos_C and pos_B < pos_C:
        # bca
        A = np.array([atom for atom in new_data if atom[5] == (B[0][5]-1)])
        pos_A = np.mean(A[:, 5])
    if pos_B > pos_C and pos_A < pos_B:
        # cab
        C = np.array([atom for atom in new_data if atom[5] == (B[0][5]+1)])
        pos_A = np.mean(np.array(A)[:, 5])
        pos_B = np.mean(np.array(B)[:, 5])
        pos_C = np.mean(C[:, 5])

    insert_plane_pos = np.mean(np.array(A)[:, 2])

    x_max = max(data[:,2])
    x_min = min(data[:,2])
    y_max = max(data[:,3])
    y_min = min(data[:,3])
    z_max = max(data[:,4])
    z_min = min(data[:,4])
    x_position = (x_max + x_min) / 2
    y_position = (y_max + y_min) / 2
    z_position = (z_max + z_min) / 2

    theta_list = list(np.linspace(0, 2 * np.pi, num_points+1))
    S_points = np.array([[insert_plane_pos,
    y_position+S_R * np.cos(theta) if abs(S_R * np.cos(theta)) > 1e-8 else y_position,
    z_position+S_R * np.sin(theta) if abs(S_R * np.sin(theta)) > 1e-8 else z_position
                    ] for theta in theta_list])
    
    # define theta we need to rotate for insert_atoms
    cos_theta = np.dot(insert_plane, target_plane) / (np.sqrt(np.power(insert_plane, 2).sum()) * np.sqrt(np.power(target_plane, 2).sum()))
    rotation_matrix = get_rotation_info(insert_plane, target_plane, cos_theta)  # type: ndarray

    # rotate the insert_points
    for point in S_points:
        point[0] -= insert_plane_pos
        point[1] -= y_position
        point[2] -= z_position
        trans_pos = np.dot(rotation_matrix, point[:].reshape(-1, 1))
        trans_pos[0] += insert_plane_pos
        trans_pos[1] += y_position
        trans_pos[2] += z_position
        point[:] = trans_pos.reshape(-1)
        point[:] += layerize_direct/2

    # define the insert points
    A_loop = [atom for atom in A if np.sum((atom[2:5] - np.array([insert_plane_pos, y_position, z_position]))**2) < S_R**2]
    insert_points = [[atom[1]] + list(atom[2:5]) for atom in A_loop]

    # resize the positions of insert_points
    for point in insert_points:
        point[1:] += layerize_direct/2

    N_insert_atom = len(insert_points)
    tri_points = np.array([[[insert_plane_pos, y_position, z_position], S_points[i], S_points[i+1]]
                           for i in range(len(S_points)-1)])
    shape = tri_points.shape
    i = 0
    # obtain line
    output_file = "model.moved.data"
    output_f = open(output_file, "w")

    input_f = open(path, "r")
    input_lines = list(input_f.readlines())

    new_atom_number = N_insert_atom + len(new_data)
    for i, line in enumerate(head_lines):
        if " atoms" in line:
            new_line = "{0} atoms\n".format(new_atom_number)
            head_lines[i] = new_line

    for i, line in enumerate(input_lines):
        output_f.writelines(head_lines)
        break
    
    for i in trange(len(new_data)):
        atom = new_data[i]
        if -30 <= atom[5] <= 30:
            # n * 3 * 3
            di_vectors = tri_points[:, :, :] - atom[2:5]
            di_vectors = di_vectors / np.sqrt((di_vectors * di_vectors).sum(2)).reshape(shape[0], 3, 1)
            u1 = di_vectors[:, 0, :]
            u2 = di_vectors[:, 1, :]
            u3 = di_vectors[:, 2, :]
            solid_angles = get_omega(u1, u2, u3)
            s = -sum(solid_angles)
            us = - s * move_b / (4 * np.pi)
            atom[2] += us[0]
            atom[3] += us[1]
            atom[4] += us[2]
    
            full_data = [int(atom[0]), int(atom[1]), atom[2], atom[3], atom[4], int(data[i][5]), int(data[i][6]),
                            int(data[i][7])]
            output_f.write(" ".join([str(item) for item in full_data]) + "\n")
        else:
            full_data = [int(atom[0]), int(atom[1]), atom[2], atom[3], atom[4], int(data[i][5]), int(data[i][6]),
                            int(data[i][7])]
            output_f.write(" ".join([str(item) for item in full_data]) + "\n")

    for i, atom in enumerate(insert_points):
        atom_id = len(new_data) + i + 1
        vx = 0
        vy = 0
        vz = 0
        trp_data = [atom_id, int(atom[0]), atom[1], atom[2], atom[3], vx, vy, vz]
        output_f.write(" ".join([str(item) for item in trp_data]) + "\n")
    output_f.writelines(tail_lines)
    for i, atom in enumerate(insert_points):
        atom_id = len(new_data) + i + 1
        vx = 0
        vy = 0
        vz = 0
        trp_data = [atom_id, vx, vy, vz]
        output_f.write(" ".join([str(item) for item in trp_data]) + "\n")


input_file = r'model.data'
burgers_vector = 1 / 2 * np.array([-1, -1, -1])
layerize_direct = np.array([-1.84465, -1.30435,  0]) # the direction of layerization
move_v1(path=input_file,
        lattice=3.195,
        x_direct=np.array([1,1,1]), # the crystal orientation of x axis
        y_direct=np.array([1, 1, -2]), # the crystal orientation of y axis
        z_direct=np.array([-1, 1, 0]), # the crystal orientation of z axis
        burgers_vector=burgers_vector, 
        layerize_direct=layerize_direct,
        target_plane=layerize_direct, # the normal direction of final S plane.
        insert_plane=np.array([-1, 0, 0]), # the normal direction of origianl inserting S plane.
        scale=5, # scale * sqrt(base) * lattice is the radius of S plane
        base=2, # scale * sqrt(base) * lattice is the radius of S plane
        num_points=48)