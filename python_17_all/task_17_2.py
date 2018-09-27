# -*- coding: utf-8 -*-
'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa0/1': {'R5': 'Fa0/1'},
        'Fa0/2': {'R6': 'Fa0/0'}}}

При этом интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''
import re
from pprint import pprint


def parse_sh_cdp_neighbors(output):
    result = {}
    hostname_regex = '(?P<hostname>\S+)[>|#]show cdp neighbors'
    neighbors_regex = '(?P<neighbor>\S+) +(?P<local_int>\w+ ?[0-9/]+) +(?:\S+ +)+ (?P<neighbors_int>\w+ ?[0-9/]+)\n'
    match = re.search(hostname_regex, output)
    hostname = match.group('hostname')
    result[hostname] = {}
    matches = re.finditer(neighbors_regex, output)
    for match in matches:
        result[hostname][match.group('local_int')] = {match.group(
            'neighbor'): match.group('neighbors_int')}
    return result


if __name__ == '__main__':
    filename = 'sh_cdp_n_sw1.txt'
    with open(filename) as f:
        pprint(parse_sh_cdp_neighbors(f.read()))