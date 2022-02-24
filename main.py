from utils.input_getter import input_getter
from rebec_program.msgserver_call_graph_gen import msgserver_call_graph_gen
from rebec_program.rebec_program_gen import rebec_program_gen
from utils.graph import graph
from rebec_program.rebeca_ast_config_gen import rebeca_ast_gen
from rebec_program.ast_gen import ast_gen
from rebec_program.property_gen import property_gen
from rebec_program.dfa_gen import dfa_gen
from rebec_program.table_gen import table_gen
from rebec_program.dfa_graph import dfa_graph_gen
# from rebec_program.draw_automata import draw_automata
from termcolor import colored
import os
from datetime import datetime
import sys
import shutil
from utils.json_reader import json_reader


def main():
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    folder = 'outputs/{}'.format(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
    os.makedirs(folder)
    shutil.copy('input.json', folder)

    jsonInputFile = sys.argv[1] if len(sys.argv) > 1 else 'input.json'
    configuration = json_reader(
        jsonInputFile) if jsonInputFile else input_getter.get_configuration()

    rebec_program_generator = rebec_program_gen(configuration)
    rebec_msgservers = rebec_program_generator.generate()

    msgserver_call_graph_generator = msgserver_call_graph_gen(
        configuration, rebec_msgservers)
    call_graph = msgserver_call_graph_generator.generate_graph()

    rebecas_graph, msgservers_graph = call_graph[1], call_graph[0]

    print(colored('Rebecas:', 'yellow', attrs=['bold']), rebecas_graph)
    print(colored('MsgServers:', 'yellow', attrs=['bold']), msgservers_graph)

    rebeca_ast_generate = rebeca_ast_gen(rebecas_graph, msgservers_graph)
    ast_config = rebeca_ast_generate.generate_ast()

    ast_generator = ast_gen(rebecas_graph, msgservers_graph, ast_config)
    ast_generator.generate()
    ast_generator.export_dot_rebec_file(folder)

    print()
    print(
        colored('Generated code is ready in output.rebec',
                'magenta',
                attrs=['bold']))

    json_output_file = open('{}/dfa.json'.format(folder), 'w', newline='\n')
    json_output_file.write('{\n')

    property_generator = property_gen(msgservers_graph, configuration)
    property_set = property_generator.get_property_set()
    property_generator.write_in_json(json_output_file)

    print()
    print(colored('Property set:', 'yellow', attrs=['bold']), property_set)

    dfa_generator = dfa_gen(property_set, configuration)
    dfa_obj = dfa_generator.get_dfa()

    print()
    print(colored('DFA:', 'yellow', attrs=['bold']))
    dfa_generator.print_automata_obj(dfa_obj)
    dfa_generator.write_automata_obj(json_output_file, dfa_obj)

    dfa_graph = dfa_graph_gen(dfa_obj, dfa_generator.backwards)

    table_generator = table_gen(rebecas_graph, dfa_graph, folder)
    table_generator.export_table()

    # draw_automata(dfa_obj, folder)
    json_output_file.write('}\n')
    json_output_file.close()


if __name__ == "__main__":
    main()
