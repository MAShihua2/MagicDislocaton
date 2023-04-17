CUR_DIR=$(cd $(dirname $0); pwd)
cd $CUR_DIR
cd ../src

############################ FCC #######################################
# fcc rotate loop 112
# python main.py \
#     --yaml_file 'F:\Projects\MagicDislocation\examples\fcc\rotate_loop_new\config.yaml'

# fcc s350 16 112
python main.py \
    --yaml_file 'F:\Projects\MagicDislocation\examples\fcc\s350_16_112\config.yaml'

# # fcc s350 1/2 110 line
# python main.py \
#     --yaml_file 'F:\Projects\MagicDislocation\examples\fcc\s350_line\config.yaml'

# # fcc s350 1/2 110 line edge
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\fcc\s350_line_edge\config.yaml'

# fcc s350 1/2 110 sin_line
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\fcc\s350_sin\config.yaml'

############################ Cubic #######################################
# cubic 110 Perovskite
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\cubic\STO_110_241_del\config.yaml'

# cubic 100 Perovskite
# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\cubic\STO_100_2_del\config.yaml'
############################ BCC #######################################
# bcc abcd b
# cd ../examples/bcc/abcd/b
# python 1_2_111_dislocation.py

# bcc abcd d
# cd ../examples/bcc/abcd/d
# python 1_2_111_dislocation.py





