import numpy as np

def get_rotation_info(insert_plane, target_plane):
    # define rotation axis
    rotation_axis = np.cross(insert_plane, target_plane)
    rotation_axis = np.sqrt(rotation_axis * rotation_axis / sum(rotation_axis * rotation_axis))
    u_x = rotation_axis[0]
    u_y = rotation_axis[1]
    u_z = rotation_axis[2]
    if isinstance(insert_plane, list):
        insert_plane = np.array(insert_plane)
    if isinstance(target_plane, list):
        target_plane = np.array(target_plane)
    cos_theta = insert_plane.dot(target_plane) / np.sqrt(sum(insert_plane * insert_plane) * sum(target_plane * target_plane))
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