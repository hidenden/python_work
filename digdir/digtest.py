#!/usr/bin/env python3

from curses.ascii import NUL
import sys
import getopt
import os
import re
import subprocess
from typing import Dict
from typing import Tuple
from typing import List

from pytest import fail


# オプション
#   -v テストツールを-v付きで実行する
#   -s サイレントモード｡ 異常があるときだけ通知する
#   -o <ファイル名> 実行結果保存ファイル｡指定がなければ保存しない
# カレントディレクトリのディレクトリリストを得る
# その中から tst_* でディレクトリのものを選別する
# tst_* の各々について
#   そのディレクトリにcdする
#   ディレクトリのエントリ一覧を得る
#   その中から tst_* のディレクトリのものを選別する
#   tst_* の各々について
#       そのディレクトリにcdする
#       opa test *.rego を実行する｡
#       実行結果の文字列は全部得る｡
#       実行結果ファイルが開いていたら､テスト名のセパレータと一緒に結果をファイルに出力する｡
#       FAILEDの文字があるかどうか調べる｡あったら記憶しておく
#       実行モードに合わせて途中経過を出力する｡(色付き)
# 全部実行が終わったあとで､FAILEDがあったかチェック
# あったらエラーを出力する｡(赤色で)
# なかったらOKを緑色で出力する
# 

ESC_RED = '\033[31m'
ESC_GREEN = '\033[32m'
ESC_END = '\033[0m'
    
def showhow():
    print("digtest.py [-v|-s] [-o outfile] [-d <topdir>] [test_name...]")
    print("  -d: テストトップディレクト｡ 指定がない場合はカレントディレクトリ")
    print("  -v: verbose mode")
    print("  -s: silent mode")
    print("  -o: テスト結果をファイルに出力する")
    print("  test_name: 実施対象テスト(例 tst_owners)｡ 省略時は全て実施")
    sys.exit(1)

def load_option(v:List[str]) -> Dict[str,str]:
    option = {"mode": "", "outfile": "", "dir": ".", "test":[]}
    try:
        shortopts = "vso:d:"
        opts, args = getopt.getopt(v, shortopts)
        for o in opts:
            flag = o[0]
            if flag == "-v":
                option["mode"] = "v"
            elif flag == "-s":
                option["mode"] = "s"
            elif flag == "-o":
                option["outfile"] = o[1]
            elif flag == "-d":
                option["dir"] = o[1]        
        if 0 < len(args):
            option["test"] = args
    except getopt.GetoptError:
        showhow()
    return option

def dig_topdir(targets:List, mode:str, outbuf:List, failbuf:List):
    filter_mode = False
    if len(targets) != 0:
        filter_mode = True

    testdirs = [d for d in os.listdir(path=".") if re.match(r'^tst_', d)]
    for td in testdirs:
        if filter_mode and not(td in targets):
            continue
            
        os.chdir(td)
        dig_testdir(td, mode, outbuf, failbuf)
        os.chdir("..")
    return

def dig_testdir(tname:str, mode:str, outbuf:List, failbuf:List):
    if mode != "s":
        print(tname, end=":")
    testdirs = [d for d in os.listdir(path=".") if re.match(r'^tst_', d)]
    testdirs.sort()
    for td in testdirs:
        os.chdir(td)
        invoke_test(td, mode, outbuf, failbuf)
        os.chdir("..")
    if mode != "s":
        print("")
    return

def invoke_test(t_name:str, mode:str, outbuf:List, failbuf:List):
    t_num = ""
    m = re.search(r'\d+$', t_name)
    if m:
        t_num = m.group()

    success = True
    command = "opa test *.rego"
    if mode == "v":
        command = command + " -v"
    cp = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode == 2:
        failbuf.append("FAIL:" + t_name)
        success = False
    elif cp.returncode == 1:
        failbuf.append("ERROR:" + t_name)
        success = False
    
    output_lines = cp.stdout.decode("utf-8").splitlines()
    err_lines = cp.stderr.decode("utf-8").splitlines()

    outbuf.append("===== " + t_name + " ======")
    for l in output_lines:
        outbuf.append(l)
    for l in err_lines:
        outbuf.append(l)

    if success == False:
        if mode != "s":
            print(ESC_RED + t_num + ESC_END, end=' ')
        else:
            print(ESC_RED + t_name + ESC_END, end=" ")
    else:
        if mode != "s":
            print(ESC_GREEN + t_num + ESC_END, end=" ")

    return

def digtest() -> int:
    option = load_option(sys.argv[1:])

    outbuf = []
    fail = []
    curdir = os.getcwd()

    os.chdir(option["dir"])
    dig_topdir(option["test"], option["mode"], outbuf, fail)
    os.chdir(curdir)

    if option["outfile"] != "":
        with open(option["outfile"], mode="w") as f:
            for l in outbuf:
                f.write(l)
                f.write("\n")
    
    if len(fail) == 0:
        print(ESC_GREEN + "All OK" + ESC_END)
    else:
        print("\nFAILED: " + str(len(fail)) +  " tests" )
        if option["mode"] != "s":
            for f in fail:
                print(ESC_RED + f + ESC_END)

    return 0

if __name__ == "__main__":
    ret = digtest()
    sys.exit(ret)