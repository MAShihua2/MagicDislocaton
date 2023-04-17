# Introduction
In this directory, we plan to create a slanted loop dislocation 1/6<112> on a FCC system, whose crystal direction is X ：-1 1 0, Y : 1 1 1, Z : 1 1 -2.

To achieve this goal, we should define a S plane perpendicular to an axis and rotate this plane. Here, we provide some parameters. In the next, we will introduce the meaning of each parameter.

# Yaml File
## data:
  input_file: path to data file.

  type: file type (data: the abbreviation of lammps-data ).

  data_line_item_num: the number of items for line containing atom positions in data file.

  pos_index: start index and end index of atom positions in data file.

  lattice: lattice constant.

  dxdydz: the layer distance of the direction of three coordinate axis. Tips: For dx,dy,dz the real layer distance is dx * lattice, dy * lattice, dz * lattice.


## layerization:
  direction: the direction of layerization, 0: x axis, 1: y axis, 2: z axis.

## s_plane:
  center_pos: the center position of S plane

  type: the shape of S plane, here is rect [rectangular].

  edge_range: the distances from center position to edges in the direction of X, Y, Z

  fix_coord: which axis of points of the loop is fixed.

  num_points: the number of points consisting the loop.

  scale: a parameter related to the length of radius of the loop. [scale * sqrt(base) * lattice].

  base: a parameter related to the length of radius of the loop. [scale * sqrt(base) * lattice].

  rotate_para: means the loop need to be rotated

    insert_plane: the normal direction of origianl inserting plane.

    target_plane: the normal direction of final S plane.

## move:
  step: the burgers vector's norm

  direction: moving direction

  move_layer_range: the range of atoms should be moved. if this parameter is N and the layer of center position of S plane if a, the atoms in layers [a-N, a+N] should be moved.


# Interface
Actions: the shape of dislocation

data file path: the path to data file

data file type: the type of data file

lattice constance: the lattice constance

structure: structure type

x_direction: the crystal oritention of x axis

y_direction: the crystal oritention of y axis

z_direction: the crystal oritention of z axis

layerization direction: the direction of layerization, 0: x axis, 1: y axis, 2: z axis.

S_plane_center_position: the center position of S plane

S_fix_coord: which axis of points of loop is fixed.

S_num_points: the number of points consisting the loop

scale: a parameter related to the length of radius of the loop. [scale * sqrt(base) * lattice].

base: a parameter related to the length of radius of the loop. [scale * sqrt(base) * lattice].

insert_plane: the normal direction of origianl inserting plane.

target_plane: the normal direction of final S plane.

dislocation shape: the detail shape of dislocation

shape range: the distances from center position to edges in the direction of X, Y, Z

Burgers vector: the detailed burgers vector, which could help produce a dislocation.

