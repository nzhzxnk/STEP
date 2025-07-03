#!/usr/bin/env python3
# solver_divide実行用に書き換えた

from common import format_tour, read_input

import solver_divide

CHALLENGES = 8

def generate_sample_output():
    for i in range(CHALLENGES):
        address_list = read_input(f'input_{i}.csv')
        address_dict = {}
        for index,address in enumerate(address_list):
            address_dict[index] = address
        divided_index_list = solver_divide.divide_city_in_zone(address_list)
        final_best_tour = solver_divide.conbine_best_tours(divided_index_list) 
        with open(f'divide_{i}.csv', 'w') as f:
            f.write(format_tour(best_tour) + '\n')

if __name__ == '__main__':
    generate_sample_output()