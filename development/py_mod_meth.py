"""Get all methods from python file/s.

This script will create a csv file (meth_func.csv) with a list of all
methods and the source module in one or more inputed python files.
"""

import ast
import csv


def write_csv(fname, olist):
   """Write output to csv file."""
    ofile = open(fname, "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
    writer.writerows(olist)


def main():
    """Get all methods from python file/s."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input .py file', nargs='+')
    args = parser.parse_args()

    mod_func = []

    for pyfile in args.input:
        tree = ast.parse(open(pyfile).read())

        methods = sorted({node.name for node in ast.walk(tree)
                          if isinstance(node, ast.FunctionDef)})
        mod_func.extend([[pyfile, methods[i]] for i in range(len(methods))])

    write_csv("meth_func.csv", mod_func)


if __name__ == '__main__':
    main()
