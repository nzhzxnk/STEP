#!/usr/bin/env python3
# solver_taboo実行用に書き換えた

from common import format_tour, read_input

import solver_taboo

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        address_list = read_input(f'input_{i}.csv')
        tour = solver_taboo.solve(address_list) # 初期経路を取得
        iteration_num , max_length_taboo = 1000, 20 #  iteration_numは改善を行う回数、max_length_tabooはタブーリストの大きさ
        best_tour = solver_taboo.taboo_search(tour, address_list, iteration_num, max_length_taboo)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(best_tour) + '\n')

if __name__ == '__main__':
    generate_sample_output()
    