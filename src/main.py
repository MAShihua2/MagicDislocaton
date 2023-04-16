import argparse
import logging
from yaml import load, Loader
from dislocation_creator_base import DislocationCreatorBase
from dislocation_creator_with_operator import DislocationCreatorWithSplaneOperator


parser = argparse.ArgumentParser()
parser.add_argument('--yaml_file', type=str, required=True)


args = parser.parse_args()

yaml_file = args.yaml_file

configs = load(open(yaml_file, "r", encoding="utf-8").read(), Loader=Loader)  # 用load方法转字典
print(configs)

# data parameters
data_config = configs['data']
# layerization
layerization_config = configs['layerization']

# s_plane
s_center_pos = configs['s_plane']['center_pos']
s_type = configs['s_plane']['type']

# move
move_direction = configs['move']['direction']
move_step = configs['move']['step']
move_layer_range = configs['move']['move_layer_range']


# if s_type == "rect":
#     dislocation_creator = DislocationCreatorBase(data_config, layerization_config)
# elif s_type == "loop":
#     dislocation_creator = DislocationCreatorWithSplaneOperator(data_config, layerization_config)

dislocation_creator = DislocationCreatorWithSplaneOperator(data_config, layerization_config) # gb
dislocation_creator.create_dislocation(move_step=move_step, move_direction=move_direction, move_layer_range=move_layer_range, s_para=configs['s_plane'])
            