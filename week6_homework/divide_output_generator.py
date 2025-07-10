#!/usr/bin/env python3
# solver_divide実行用に書き換えた

from common import format_tour, read_input

import solver_divide

CHALLENGES = 8

def generate_sample_output():
    for i in range(CHALLENGES):
        tsp_divide = solver_divide.TravelingSalesman()
        tsp_divide.address_list = read_input(f'input/input_{i}.csv')
        for index,address in enumerate(tsp_divide.address_list):
            tsp_divide.address_dict[index] = address
        tsp_divide.divide_city_in_zone()
        final_best_tour = tsp_divide.conbine_best_tours() 
        with open(f'divide_{i}.csv', 'w') as f:
            f.write(format_tour(final_best_tour) + '\n')

if __name__ == '__main__':
    generate_sample_output()

'''
    hireling
    外スコープと内側スコープで同じ変数名は使わない、ダメではないけど混乱の元
    def calc_range(address_list):
  min_x, min_y = address_list_[0]
  max_x, max_y = min_x, min_y
  for point in address_list:
    if min_x > point[0]: min_x = point[0]
    if max_x < point[0]: max_x = point[0]
    ...
    min_x = min(min_x, point[0])
    max_x = max(max_x, point[0])
    min_y = min(min_y, point[1])
    max_y = max(max_y, point[1])
  return min_x, min_y, max_x, max_y
  ノードのクラスタ
  インデックスはなるべく使わないで
  '''