CUR_DIR=$(cd $(dirname $0); pwd)
cd $CUR_DIR
cd ../../src

python main.py \
    --yaml_file 'D:\DislocationProject\MagicDislocation\examples\fcc\STO_110_241_del\config.yaml'

# python main.py \
#     --yaml_file 'D:\DislocationProject\MagicDislocation\examples\fcc\STO_100_2_del\config.yaml'
