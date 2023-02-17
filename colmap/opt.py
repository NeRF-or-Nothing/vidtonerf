import configargparse

def config_parser(cmd=None):
    parser = configargparse.ArgumentParser()

    parser.add_argument('--config', is_config_file = True, default = 'configs/default.txt',
                        help = 'config file path')
                        
    parser.add_argument('--local_run', type = bool, default = False,
                        help = 'run colmap worker locally')

    parser.add_argument('--input_data_path', default = 'data/inputs/video/input.mp4',
                        help = 'input data path for local runs')

    if cmd is not None:
        return parser.parse_args(cmd)
    else:
        return parser.parse_args()