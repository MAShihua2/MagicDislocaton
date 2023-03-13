CUR_DIR=$(cd $(dirname $0); pwd)
cd $CUR_DIR
cd ../src

# cubic 110 Perovskite
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\cubic\STO_110_241_del\config.yaml'

# cubic 100 Perovskite
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\cubic\STO_100_2_del\config.yaml'


# bcc 111
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\bcc\111\config.yaml'


# fcc rotate loop 112
python main.py \
    --yaml_file 'D:\DislocationProject\MagicDislocation\examples\fcc\rotate_loop_112\config.yaml'

# fcc cross loop 001
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\fcc\cross_loop_001\config.yaml'

