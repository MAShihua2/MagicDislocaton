from gooey import Gooey, GooeyParser
import numpy as np
from dislocation_creator_with_operator import DislocationCreatorWithSplaneOperator

def get_eval(string):
    return [eval(v) for v in string.split(",")]


@Gooey
def main():
    parser = GooeyParser(description="Welcome to Use MagicDislocation")

    subs_list = parser.add_subparsers(help="cmms", dest="command")
    sub_action0 = subs_list.add_parser("Splane-line/rectangular")
    sub_action0.add_argument("data_file_path", help="", widget="FileChooser")
    sub_action0.add_argument("data_file_type", help="", widget="Dropdown", default="lammps-data", choices=["lammps-data", "vasp-poscar"])
    sub_action0.add_argument("lattice_constance", help="", widget="TextField")
    sub_action0.add_argument("structure_type", help="", widget="Dropdown", default="FCC", choices=["BCC", "FCC", "Cubic"])
    sub_action0.add_argument("x_direct", help="", widget="TextField")
    sub_action0.add_argument("y_direct", help="", widget="TextField")
    sub_action0.add_argument("z_direct", help="", widget="TextField")

    sub_action0.add_argument("layerization_direction", help="", widget="Dropdown", choices=['0', '1', '2'])

    sub_action0.add_argument("S_plane_center_position", help="", default="-1")
    sub_action0.add_argument("dislocation_shape", help="", widget="Dropdown", choices=["rect", "line"])
    sub_action0.add_argument("shape_range", help="", widget="TextField")

    sub_action0.add_argument("Burgers_vector", help="", widget="TextField")

    sub_action1 = subs_list.add_parser("Splane-Sin")
    sub_action1.add_argument("data_file_path", help="", widget="FileChooser")
    sub_action1.add_argument("data_file_type", help="", widget="Dropdown", default="lammps-data", choices=["lammps-data", "vasp-poscar"])
    sub_action1.add_argument("lattice_constance", help="", widget="TextField")
    sub_action1.add_argument("structure_type", help="", widget="Dropdown", default="FCC", choices=["BCC", "FCC", "Cubic"])
    sub_action1.add_argument("x_direct", help="", widget="TextField")
    sub_action1.add_argument("y_direct", help="", widget="TextField")
    sub_action1.add_argument("z_direct", help="", widget="TextField")

    sub_action1.add_argument("layerization_direction", help="", widget="Dropdown", choices=['0', '1', '2'])
    
    sub_action1.add_argument("S_plane_center_position", help="", default="-1")
    sub_action1.add_argument("dislocation_shape", help="the shape of dislocation", default="sin")
    sub_action1.add_argument("S_fix_coord", help="the fixed axis", default="0")
    sub_action1.add_argument("S_sin_num_points", help="number of Sin edge points", default="32")
    sub_action1.add_argument("S_sin_A", help="A of Asin(wx)", default="10")
    sub_action1.add_argument("S_sin_omega", help="A of Asin(wx)", default="8")
    sub_action1.add_argument("S_sin_start", help="the point index of sin's start", default="1")
    sub_action1.add_argument("S_sin_end", help="the point index of sin's end", default="2")
    
    sub_action1.add_argument("shape_range", help="", widget="TextField")

    sub_action1.add_argument("Burgers_vector", help="", widget="TextField")

    sub_action2 = subs_list.add_parser("Splane-loop")

    sub_action2.add_argument("data_file_path", help="", widget="FileChooser")
    sub_action2.add_argument("data_file_type", help="", widget="Dropdown", default="lammps-data", choices=["lammps-data", "vasp-poscar"])
    sub_action2.add_argument("lattice_constance", help="", widget="TextField")
    sub_action2.add_argument("structure_type", help="", widget="Dropdown", default="FCC", choices=["BCC", "FCC", "Cubic"])
    sub_action2.add_argument("x_direct", help="", widget="TextField")
    sub_action2.add_argument("y_direct", help="", widget="TextField")
    sub_action2.add_argument("z_direct", help="", widget="TextField")

    sub_action2.add_argument("layerization_direction", help="", widget="Dropdown", choices=['0', '1', '2'])

    sub_action2.add_argument("S_plane_center_position", help="", widget="TextField")
    sub_action2.add_argument("S_fix_coord", help="the fixed axis", default="0")
    sub_action2.add_argument("dislocation_shape", help="", widget="Dropdown", choices=["loop"])
    sub_action2.add_argument("S_num_points", help="", widget="TextField")
    sub_action2.add_argument("scale", help="", widget="TextField")
    sub_action2.add_argument("base", help="", widget="TextField")
    
    # sub_action2.add_argument("rotate_cos_theta", help="", widget="TextField")
    # sub_action2.add_argument("margin_flag", help="", widget="Dropdown", choices=[1, 0])
    # sub_action2.add_argument("margin_scale", help="", widget="TextField")
    # sub_action2.add_argument("margin_base", help="", widget="TextField")
    sub_action2.add_argument("target_plane", help="", widget="TextField", default="0,0,0")
    sub_action2.add_argument("insert_plane", help="", widget="TextField", default="0,0,0")

    sub_action2.add_argument("Burgers_vector", help="", widget="TextField")

    args = parser.parse_args()
    print(args, flush=True)

    configs = dict()
    configs['data'] = dict()
    configs['data']['input_file'] = args.data_file_path
    configs['data']['type'] = 'data' if  args.data_file_type == "lammps-data" else "data"
    configs['data']['lattice'] = eval(args.lattice_constance)
    configs['data']['pos_index'] = [3, 6] if args.structure_type == "Cubic" else [2, 5]
    configs['data']['x_direct'] = get_eval(args.x_direct)
    configs['data']['y_direct'] = get_eval(args.y_direct)
    configs['data']['z_direct'] = get_eval(args.z_direct)
    configs['data']['data_line_item_num'] = 6 if args.structure_type == "Cubic" else 8

    configs['layerization'] = dict()
    configs['layerization']['direction'] = int(eval(args.layerization_direction))

    if args.structure_type == "FCC":
        if configs['data']['x_direct'][0] % 2 != 0 and configs['data']['x_direct'][1] % 2 != 0 and configs['data']['x_direct'][2] % 2 != 0:
            dx = 1 / np.sqrt(np.power(np.array(configs['data']['x_direct']),2).sum())
        else:
            dx = 1 / np.sqrt(np.power(np.array(configs['data']['x_direct']),2).sum())
            dx = dx / 2
        if configs['data']['y_direct'][0] % 2 != 0 and configs['data']['y_direct'][1] % 2 != 0 and configs['data']['y_direct'][2] % 2 != 0:
            dy = 1 / np.sqrt(np.power(np.array(configs['data']['y_direct']), 2).sum())
        else:
            dy = 1 / np.sqrt(np.power(np.array(configs['data']['y_direct']), 2).sum())
            dy = dy / 2
        if configs['data']['z_direct'][0] % 2 != 0 and configs['data']['z_direct'][1] % 2 != 0 and configs['data']['z_direct'][2] % 2 != 0:
            dz = 1 / np.sqrt(np.power(np.array(configs['data']['z_direct']), 2).sum())
        else:
            dz = 1 / np.sqrt(np.power(np.array(configs['data']['z_direct']), 2).sum())
            dz = dz / 2
    elif args.structure_type == "BCC":
        if (abs(configs['data']['x_direct'][0]) + abs(configs['data']['x_direct'][1]) + abs(configs['data']['x_direct'][2])) % 2 == 0:
            dx = 1 / np.sqrt(np.power(np.array(configs['data']['x_direct']),2).sum())
        else:
            dx = 1 / np.sqrt(np.power(np.array(configs['data']['x_direct']),2).sum())
            dx = dx / 2
        if (abs(configs['data']['y_direct'][0]) + abs(configs['data']['y_direct'][1]) + abs(configs['data']['y_direct'][2])) % 2 == 0:
            dy = 1 / np.sqrt(np.power(np.array(configs['data']['y_direct']), 2).sum())
        else:
            dy = 1 / np.sqrt(np.power(np.array(configs['data']['y_direct']), 2).sum())
            dy = dy / 2
        if (abs(configs['data']['z_direct'][0]) + abs(configs['data']['z_direct'][1]) + abs(configs['data']['z_direct'][2])) % 2 == 0:
            dz = 1 / np.sqrt(np.power(np.array(configs['data']['z_direct']), 2).sum())
        else:
            dz = 1 / np.sqrt(np.power(np.array(configs['data']['z_direct']), 2).sum())
            dz = dz / 2
    elif args.structure_type == "Cubic":
        dx = 1 / np.sqrt(np.power(np.array(configs['data']['x_direct']),2).sum())
        dy = 1 / np.sqrt(np.power(np.array(configs['data']['y_direct']), 2).sum())
        dz = 1 / np.sqrt(np.power(np.array(configs['data']['z_direct']), 2).sum())
        dx = dx / 2
        dy = dy / 2
        dz = dz / 2

    configs['data']['dxdydz'] = [dx, dy, dz]
    configs['s_plane'] = dict()
    configs['s_plane']['type'] = args.dislocation_shape
    configs['s_plane']['center_pos'] = get_eval(args.S_plane_center_position)
    if args.dislocation_shape == "line" or args.dislocation_shape == "rect" or args.dislocation_shape == "sin":
        configs['s_plane']['edge_range'] = get_eval(args.shape_range)
    if args.dislocation_shape == "sin":
        configs['s_plane']['sin'] = dict()
        configs['s_plane']['sin']['num_points'] = int(eval(args.S_sin_num_points))
        configs['s_plane']['sin']['fix_coord'] = int(eval(args.S_fix_coord))
        configs['s_plane']['sin']['A'] = float(eval(args.S_sin_A))
        configs['s_plane']['sin']['omega'] = float(eval(args.S_sin_omega))
        configs['s_plane']['sin']['start'] = int(eval(args.S_sin_start))
        configs['s_plane']['sin']['end'] = int(eval(args.S_sin_end))

    if args.dislocation_shape == "loop":
        configs['s_plane']['num_points'] = int(eval(args.S_num_points))
        configs['s_plane']['fix_coord'] = int(eval(args.S_fix_coord))
        configs['s_plane']['scale'] = int(eval(args.scale))
        configs['s_plane']['base'] = int(eval(args.base))

        if args.insert_plane != "0,0,0":
            configs['s_plane']['rotate_para'] = dict()
            configs['s_plane']['rotate_para']['insert_plane'] = get_eval(args.insert_plane)
            configs['s_plane']['rotate_para']['target_plane'] = get_eval(args.target_plane)
            configs['s_plane']['rotate_para']['cos_theta'] = 0
            configs['s_plane']['rotate_para']['cross'] = False
            configs['s_plane']['rotate_para']['margin_flag'] = 0
            configs['s_plane']['rotate_para']['margin_base'] = 0
            configs['s_plane']['rotate_para']['margin_scale'] = [1, 12]



    configs['move'] = dict()
    dislocation = get_eval(args.Burgers_vector)
    step = dislocation[0] / dislocation[1] * np.sqrt(dislocation[2]**2 + dislocation[3]**2 + dislocation[4]**2)
    A_matrix = np.array([[configs['data']['x_direct'][0], configs['data']['y_direct'][0], configs['data']['z_direct'][0]],
                         [configs['data']['x_direct'][1], configs['data']['y_direct'][1], configs['data']['z_direct'][1]],
                         [configs['data']['x_direct'][2], configs['data']['y_direct'][2], configs['data']['z_direct'][2]]])
    b = np.array([dislocation[2], dislocation[3], dislocation[4]])
    move_direction = np.linalg.solve(A_matrix, b)
    print("The move direction is: ", move_direction.tolist())
    configs['move']['step'] = step
    configs['move']['direction'] = move_direction.tolist()
    configs['move']['move_layer_range'] = 30


    # data parameters
    data_config = configs['data']
    # layerization
    layerization_config = configs['layerization']
    # move
    move_direction = configs['move']['direction']
    move_step = configs['move']['step']
    move_layer_range = configs['move']['move_layer_range']


    dislocation_creator = DislocationCreatorWithSplaneOperator(data_config, layerization_config) # gb
    dislocation_creator.create_dislocation(move_step=move_step, move_direction=move_direction, move_layer_range=move_layer_range, s_para=configs['s_plane'])
            
    
if __name__ == '__main__':
    main()
