#!/usr/bin/env python3

import sys
import getopt
import os
import json
from typing import Dict
from typing import List


def showhow():
    print("configfilter.py -t tpldir -o outdir [-p <pattern>] [-v] <key-value.json>")
    print("  -t: 設定ファイルのテンプレートが格納されたディレクトリ")
    print("  -o: 処理された設定ファイルの出力先ディレクトリ")
    print("  -p: パラメータ部を示すパターン｡デフォルトは ##")
    print("  -v: verboseモード")
    print("  key-value.json: パラメータの実値が定義されたjsonファイル")
    sys.exit(1)

def load_option(v:List[str]) -> Dict:
    option = {"tpldir": "", "outdir": "", "pattern": "##", "verbose":False, "kv": ""}
    try:
        shortopts = "t:o:p:v"
        opts, args = getopt.getopt(v, shortopts)
        for o in opts:
            flag = o[0]
            if flag == "-v":
                option["verbose"] = True
            elif flag == "-t":
                option["tpldir"] = o[1]
            elif flag == "-o":
                option["outdir"] = o[1]
            elif flag == "-p":
                option["pattern"] = o[1]
        if len(args) != 1:
            showhow()
        option["kv"] = args[0]
        if option["verbose"]:
            print("Template Dir:", option["tpldir"])
            print("Output Dir:", option["outdir"])
            print("Patten:", option["pattern"])
            print("Key-Value-JSON:", option["kv"])

        # Check parameters.
        if not os.path.isdir(option["tpldir"]):
            print("Not a directory:", option["tpldir"])
            showhow()

        if not os.path.isdir(option["outdir"]):
            print("Not a directory:", option["tpldir"])
            showhow()

        if option["tpldir"] == option["outdir"]:
            print("Can't specify same directories -t and -o")
            showhow()

        if not os.path.isfile(option["kv"]):
            print("Invalid path is specified:", option["kv"])
            showhow()
            
    except getopt.GetoptError:
        showhow()
    return option


class ConfigFilter:
    def __init__(self, tpldir:str, outdir:str, kv:str):
        self.tpldir = tpldir
        self.outdir = outdir
        self.verbose = False
        self.pattern = "##"
        self.kv:List[KeyWord] = []
        json_file = open(kv, 'r')
        kv_json = json.load(json_file)
        for k in kv_json:
            keyword = KeyWord(k, kv_json[k], self.pattern)
            self.kv.append(keyword)

    def set_verbose(self, v:bool) -> None:
        self.verbose = v

    def set_pattern(self, p:str) -> None:
        self.pattern = p

    def start(self) -> None:
        if self.verbose:
            print(self.kv)

        conf_paths = os.listdir(path=self.tpldir)
        for c in conf_paths:
            path = self.tpldir + '/' + c
            if os.path.isfile(path):
                if self.verbose:
                    print("File:" + c + " to " + self.outdir)
                cg = ConfigGenerator(c, self.tpldir, self.outdir, self.pattern, self.kv, self.verbose)
                cg.start()

    def check(self) -> None:
        for kw in self.kv:
            kw.print_result(self.verbose)

class KeyWord:
    def __init__(self, key:str, value:str, pattern:str):
        self.key = pattern + key + pattern
        self.value = value
        self.count: int = 0
        self.replaced = False

    def replace(self, line:str) -> str:
        if self.key in line:
            self.replaced = True
            self.count += 1
            newline = line.replace(self.key, self.value)
            return newline
        else:
            self.replaced = False
            return line

    def is_replaced(self) -> bool:
        return self.replaced

    def print_result(self, verbose:bool) -> None:
        if self.count == 0:
            print("WARN:" + self.key + " is not used in any files")
        elif verbose:
            print(self.key + " used " + str(self.count) + " times")

class ConfigGenerator:
    def __init__(self, fname:str, indir:str, outdir:str, pattern:str, kv:List[KeyWord], verbose:bool):
        in_path = indir + '/' + fname
        self.indata = []
        self.outdata = []
        with open(in_path, 'r') as infile:
            self.indata = infile.readlines()

        self.outpath = outdir + '/' + fname
        if os.path.exists(self.outpath):
            raise Exception("Output file already exists:" + self.outpath)
        
        self.pattern = pattern
        self.kv = kv
        self.verbose = verbose

    def start(self) -> None:
        self.convert_lines()
        self.save_conf()

    def convert_lines(self) -> None:
        for l in self.indata:
            if self.pattern in l:
                if self.verbose:
                    print("Replace:" + l, end="", flush=True)
                newline = self.replace_keywords(l)
                if self.pattern in newline:
                    print("WARN:NOT REPLACED:" + newline, end="")
                self.outdata.append(newline)
            else:
                self.outdata.append(l)

    def save_conf(self) -> None:
        with open(self.outpath, "w") as f:
            for l in self.outdata:
                f.write(l)

    def replace_keywords(self, line:str) -> str:
        for kw in self.kv:
            line = kw.replace(line)
        return line

if __name__ == "__main__":
    option = load_option(sys.argv[1:])

    cf = ConfigFilter(option["tpldir"], option["outdir"], option["kv"])
    cf.set_verbose(option["verbose"])
    cf.set_pattern(option["pattern"])

    try:
        cf.start()
        cf.check()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
