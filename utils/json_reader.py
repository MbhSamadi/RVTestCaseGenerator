import json
from rebec_program.rebec_program_conf import rebec_program_conf


def json_reader(json_input_file):
    file_json = open(json_input_file, 'r')
    # json_string = file_json.read()
    # print('test', json_string)
    json_out = json.load(file_json)
    print(json_out)
    return rebec_program_conf(
        json_out['rebec_count'], json_out['max_msgservers_count'],
        json_out['max_msgservers_seq'], json_out['property_length'],
        json_out['non_causality_count'], json_out['causality_count'],
        json_out['backwards_count'],json_out['maximum_method_calls'])
