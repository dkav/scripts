"""Get all function calls from python file/s.

This script will create a csv file (func_list.csv) with a list of all
function calls in one or more inputed python files, reporting the number
of times a function is called. For multiple files it will output a second
csv file (func_mod.csv) with the count summarized by module.

Based on code by Suhas S G. See -
https://suhas.org/function-call-ast-python
The MIT License (MIT)
Copyright (c) 2016 Suhas S G <jargnar@gmail.com>
"""

import ast
from collections import Counter, deque
import csv


class FuncCallVisitor(ast.NodeVisitor):

    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    """Get function calls."""
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)

    return func_calls


def write_csv(fname, olist):
    """Write output to csv file."""
    ofile = open(fname, "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
    writer.writerows(olist)


def main():
    """Get all function calls from python file."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input .py file', nargs='+')
    args = parser.parse_args()

    func_list = []
    func_mod = []

    if len(args.input) == 1:
        func_list.extend(
            get_func_calls(ast.parse(open(args.input[0]).read())))

    else:
        for pyfile in args.input:
            func = get_func_calls(ast.parse(open(pyfile).read()))

            func_list.extend(func)

            func_cnt = sorted(Counter(func).items())
            func_mod.extend([[pyfile, func_cnt[i][0],
                              func_cnt[i][1]] for i in range(len(func_cnt))])

        write_csv("func_mod.csv", func_mod)

    func_list = sorted(Counter(func_list).items())
    write_csv("func_list.csv", func_list)


if __name__ == '__main__':
    main()
