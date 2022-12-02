from utils import file
from object.env import Env
from object.interface import interface as Interface

if __name__ == '__main__':
    yaml_data = file.get_yaml_data('./yaml/interface.yaml')

    env = Env.parse_obj(yaml_data.pop(0)['env'])
    interface = Interface.parse_obj(yaml_data.pop(0))
    correct, error = interface.get_all_correct_data_and_all_error_list()
    request_list = interface.get_all_requests(correct, error, env)

    for i in request_list:
        print(i)

