#!/usr/bin/python3

import getopt
from re import T
import sys
from typing import Dict
from typing import Tuple
from typing import List

def showhow():
    print("getopt_sample [-c][-r][-u][-d] <pattern>")
    sys.exit(1)

def show_mode(crud_mode:Dict, pattern:str):
    print("PATTERN:" + pattern)
    for k in crud_mode:
        print(" " + k + ":" + str(crud_mode[k]))

def getopt_sample():
    crud_mode, pattern = load_option(sys.argv[1:])
    show_mode(crud_mode, pattern)
    parse_pattern(pattern)

def load_option(v:List[str]) -> Tuple[Dict[str,bool], str]:
    crud_mode = {"create": False, "read": False, "update": False, "delete": "False"}
    pattern = ""

    if len(v) == 0:
        showhow()

    shortopts = "crud"
    try:
        opts, args = getopt.getopt(v, shortopts)
    except getopt.GetoptError:
        showhow()

    if len(opts) == 0:
        crud_mode["read"] = True
    else:
        for o in opts:
            flag = o[0]
            if flag == "-c":
                crud_mode["create"] = True
            elif flag == "-r":
                crud_mode["read"] = True
            elif flag == "-u":
                crud_mode["update"] = True
            elif flag == "-d":
                crud_mode["delete"] = True

    pattern = args[0]
    return crud_mode,pattern

def parse_pattern(pattern:str):
    # _より後ろは切り落とす
    p1 = pattern.split('_')[0]

    # 'C' で分割する｡
    raw_rules = p1.split('C')
    if raw_rules[0] == '':
        raw_rules.pop(0)
    
    rules = []
    for rule_pattern in raw_rules:
        a_rule = list(rule_pattern)
        rules.append({"condition": a_rule[0], "permitted": a_rule[1:]})

    # 分割したそれぞれについて parse_rule()を呼び出す｡
    for r in rules:
        parse_rule(r)

    return

def parse_rule(rule:map):
    print("parse_rule:" + str(rule))
    return



if __name__ == '__main__':
    getopt_sample()
    sys.exit(0)
