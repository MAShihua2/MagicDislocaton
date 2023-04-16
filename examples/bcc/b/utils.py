import numpy as np
import math

def read_dump(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [line for line in lines if line.strip() is not None]
        result = []
        for line in lines[9:]:
            # convert str to number
            result.append([eval(item) for item in line.split()])
        return np.array(result)


def read_data(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        result = []
        atom_start_index = 0
        atom_end_index = 1000000000
        for i, line in enumerate(lines):
            # convert str to number
            items = line.split()
            if len(items) == 8:
                if atom_start_index == 0:
                    atom_start_index = i
                result.append([eval(item) for item in line.split()])
            if line.strip() == "Velocities":
                atom_end_index = i-1
        head_lines = lines[:atom_start_index]
        tail_lines = lines[atom_end_index:]
        return np.array(result), head_lines, tail_lines

def define_plane_(data, direct):

    direct = np.array(direct)
    direct_num = np.sqrt(np.sum(direct**2))
    data_pos = np.array(data[:, 2:5])
    dot_product = [round(item, 1) for item in list(np.sum(data_pos * direct, axis=1) / direct_num)]
    
    layer_ranges = list(sorted(list(set(dot_product)), reverse=False))
    print(layer_ranges)
    num_plane = len(layer_ranges)
    print("Number of Layers", num_plane)
    plane_types = [0, 1, 2] * num_plane #（111）typeA,B,C用0,1,2表示*length后，0是A，length是B，2*len是C
    plane_types = plane_types[:num_plane]
    odd_flag = num_plane % 2 != 0 #%除法取余数，判断奇偶数
    new_data = np.concatenate((data, np.zeros((len(data), 2))), axis=1)
    
    #np.zeros返回一个给定形状和类型的用0填充的数组
    for atom, pos_v in zip(new_data, dot_product):
        num_layer = layer_ranges.index(pos_v)
        # atom layer type
        atom[6] = plane_types[num_layer] #把atom原子面typeappend
        if odd_flag:
            # layer num
            atom[5] = num_layer - int(num_plane / 2) #偶数面，atom[5]为上半部分的层数，s面为O面
        else:
            atom[5] = num_layer - int(num_plane / 2)
            if atom[5] >= 0:                            #奇数面，atom[5]是上半部分加一层0面的层数
                atom[5] += 1

    # define needed A, B, C and inserted plane
    A, B, C, s_y = [], [], [], 0
    if odd_flag:
        last_plane = [atom for atom in new_data if atom[5] == -1]  #怎么会有-1,0,1呢？
        middle_plane = [atom for atom in new_data if atom[5] == 0]
        top_plane = [atom for atom in new_data if atom[5] == 1]
        abc_plane_type = "".join([str(int(last_plane[0][6])), str(int(middle_plane[0][6])), str(int(top_plane[0][6]))])
        print(abc_plane_type)
        if abc_plane_type == "012":
            A = last_plane
            B = middle_plane
            C = top_plane
            pos_C = sum(layer_ranges[1 + int(num_plane / 2)]) / 2
            pos_A = sum(layer_ranges[-1 + int(num_plane / 2)]) / 2
            pos_B = sum(layer_ranges[0 + int(num_plane / 2)]) / 2
        elif abc_plane_type == "120":
            B = last_plane
            C = middle_plane
            A = top_plane
            pos_C = sum(layer_ranges[0 + int(num_plane / 2)]) / 2
            pos_A = sum(layer_ranges[1 + int(num_plane / 2)]) / 2
            pos_B = sum(layer_ranges[-1 + int(num_plane / 2)]) / 2
        elif abc_plane_type == "201":
            C = last_plane
            A = middle_plane
            B = top_plane
            pos_C = layer_ranges[-1 + int(num_plane / 2)]
            pos_A = layer_ranges[0 + int(num_plane / 2)]
            pos_B = layer_ranges[1 + int(num_plane / 2)]
        print("Finishing")
    else:
        last_plane = [atom for atom in new_data if atom[5] == -1]  #怎么会有-1,0,1呢？
        middle_plane = [atom for atom in new_data if atom[5] == 1]
        top_plane = [atom for atom in new_data if atom[5] == 2]
        abc_plane_type = "".join([str(int(last_plane[0][6])), str(int(middle_plane[0][6])), str(int(top_plane[0][6]))])
        print(abc_plane_type)
        if abc_plane_type == "012":
            A = last_plane
            B = middle_plane
            C = top_plane
            pos_C = layer_ranges[2 + int(num_plane / 2)]
            pos_A = layer_ranges[0 + int(num_plane / 2)]
            pos_B = layer_ranges[1 + int(num_plane / 2)]
        elif abc_plane_type == "120":
            B = last_plane
            C = middle_plane
            A = top_plane
            pos_C = layer_ranges[1 + int(num_plane / 2)]
            pos_A = layer_ranges[2 + int(num_plane / 2)]
            pos_B = layer_ranges[0 + int(num_plane / 2)]
        elif abc_plane_type == "201":
            C = last_plane
            A = middle_plane
            B = top_plane
            pos_C = layer_ranges[0 + int(num_plane / 2)]
            pos_A = layer_ranges[1 + int(num_plane / 2)]
            pos_B = layer_ranges[2 + int(num_plane / 2)]
        print("Finishing")

    return A, B, C, pos_A, pos_B, pos_C, new_data 


def get_omega(u1, u2, u3):
    # u1: n * 3
    eps = 1e-12  #eps是什么？
    denominator = 1 + (u2 * u3).sum(1) + (u1 * u3).sum(1) + (u1 * u2).sum(1)
    numerator = (np.cross(u2, u3) * u1).sum(1)
    s_tri = np.arctan(numerator / denominator)

    mask_neg_denominator = np.where(denominator < 0, 1, 0)
    mask_neg_numerator = np.where(numerator < 0, -np.pi, np.pi)
    delta = mask_neg_denominator * mask_neg_numerator
    s_tri += delta

    eps_denominator_mask = np.where(abs(denominator) < eps, 1, 0)
    eps_numerator_mask = np.where(abs(numerator) < eps, 1, 0)
    eps_mask = eps_denominator_mask * eps_numerator_mask
    s_tri = s_tri * (1 - eps_mask)
    eps_delta = eps_mask * 0.5 * np.pi
    s_tri += eps_delta
    return 2 * s_tri


def get_rotation_info(insert_plane, target_plane, cos_theta):
    # define rotation axis
    rotation_axis = np.cross(insert_plane, target_plane)
    print(rotation_axis)
    rotation_axis = rotation_axis / np.sqrt(sum(rotation_axis * rotation_axis))
    print(rotation_axis)
    u_x = rotation_axis[0]
    u_y = rotation_axis[1]
    u_z = rotation_axis[2]
    # define rotation theta
    sin_theta = np.sqrt(1 - cos_theta * cos_theta)
    rotation_matrix = np.array([[cos_theta + u_x * u_x * (1 - cos_theta), u_x * u_y * (1 - cos_theta) - u_z * sin_theta,
                                 u_x * u_z * (1 - cos_theta) + u_y * sin_theta],
                                [u_y * u_x * (1 - cos_theta) + u_z * sin_theta, cos_theta + u_y * u_y * (1 - cos_theta),
                                 u_y * u_z * (1 - cos_theta) - u_x * sin_theta],
                                [u_z * u_x * (1 - cos_theta) - u_y * sin_theta,
                                 u_z * u_y * (1 - cos_theta) + u_x * sin_theta,
                                 cos_theta + u_z * u_z * (1 - cos_theta)]
                                ])
    return rotation_matrix

