<<<<<<< HEAD
# MagicDislocation
This is a flexible dislocation creation tool based on Python3


# What can MagicDislocation do?
It could move atoms according to given direction and S plane to produce a new system containing a certain dislocation.

# What information is needed?

In detail, when users hope to produce a certain dislocation, they should provide information related to system, S-plane, dislocation's Burgers Vector, Then, atoms will move to certain positions.

For the system, users should give the lattice constant, data file type, data file path, structure type and the direction of each axis.

S plane is related to the shape and range of dislocation. If the S plane is a circle, the dislocation would be a loop. If the S plane is a rectangle, the dislocation would also be a rectangle loop. When trying to create a dislocation, the user should pass the $\bf{center}$  $\bf{position}$ of the S plane to the interface. Also, if the S plane is a rectangle, the user should tell the distances from center position to edges in the direction of X, Y, Z. If the S plane is a loop, the user should tell the radius of this loop. Besides, We default to the S-plane being perpendicular to some coordinate axis. If the S-plane is not perpendicular to the coordinate axis, the user can first construct an S plane perpendicular to the axes and then produce the desired S-plane by means of a rotation. This, of course, requires the user to provide the $\bf{orientation}$ of the initial S plane and the final S plane.

The Burgers vector <h, k, l> represents the moving direction and displace of atoms. Considering there are several different moving directions for a Burgers vector, users are required to give a detailed direction such as [h, k, l] or [-h, -k, l]. The detailed direction should be determined according to the S plane and axis's modeling direction.


# How to Run

## Method 1: Passing parameters via yaml file
`
cd examples
`

and then make a new directory to store your data,

and then you could pass the parameters related to your operations,

here, we store these parameters in the form of yaml file,

you could create your yaml file by referring these exisiting yaml files.

Then, you could start the shell script in `examples` directory

`
bash run.sh
`


## Method 2: Passing parameters via interface
`
cd src
`

`
python vis_main.py
`

Passing related parameters via the interface.


# Examples
Detailed examples could be found in examples files. Users could create their own case via refering these examples.
=======

#If you use this program to construct dislocation, please cite:
Shihua MA, Wei SHAO, Shijun ZHAO. MagicDislocation: A Flexible Dislocations Construction Toolkit Based on Continuum Dislocation Theory. COMPUTER PHYSICS COMMUNICATIONS. Submitted
 

# MagicDislocation
This is a flexible dislocation creation tool based on Python3


# What can MagicDislocation do?
It could move atoms according to given direction and S plane to produce a new system containing a certain dislocation.

# What information is needed?

In detail, when users hope to produce a certain dislocation, they should provide information related to system, S-plane, dislocation's Burgers Vector, Then, atoms will move to certain positions.

For the system, users should give the lattice constant, data file type, data file path, structure type and the direction of each axis.

S plane is related to the shape and range of dislocation. If the S plane is a circle, the dislocation would be a loop. If the S plane is a rectangle, the dislocation would also be a rectangle loop. When trying to create a dislocation, the user should pass the $\bf{center}$  $\bf{position}$ of the S plane to the interface. Also, if the S plane is a rectangle, the user should tell the distances from center position to edges in the direction of X, Y, Z. If the S plane is a loop, the user should tell the radius of this loop. Besides, We default to the S-plane being perpendicular to some coordinate axis. If the S-plane is not perpendicular to the coordinate axis, the user can first construct an S plane perpendicular to the axes and then produce the desired S-plane by means of a rotation. This, of course, requires the user to provide the $\bf{orientation}$ of the initial S plane and the final S plane.

The Burgers vector <h, k, l> represents the moving direction and displace of atoms. Considering there are several different moving directions for a Burgers vector, users are required to give a detailed direction such as [h, k, l] or [-h, -k, l]. The detailed direction should be determined according to the S plane and axis's modeling direction.


# How to Run

## Method 1: Passing parameters via yaml file
`
cd examples
`

and then make a new directory to store your data,

and then you could pass the parameters related to your operations,

here, we store these parameters in the form of yaml file,

you could create your yaml file by referring these existing yaml files.

Then, you could start the shell script in `examples` directory

`
bash run.sh
`
Or 

python  main.py --yaml_file './config.yaml (yaml_file path)'


## Method 2: Passing parameters via interface
`
cd src
`

`
python vis_main.py
`

Passing related parameters via the interface.


# Examples
Detailed examples could be found in examples files. Users could create their own case via referring these examples.
>>>>>>> de2d02f6b59fc072d8386febfd84b80e1f0d12aa
