import argparse

parser = argparse.ArgumentParser()
parser.add_argument("arg", nargs='*')
args = [x for x in parser.parse_args().arg]
if args:
    if len(args) == 1:
        print('TOO FEW PARAMS')
    elif len(args) > 2:
        print('TOO MANY PARAMS')
    else:
        try:
            print(int(args[0]) + int(args[1]))
        except Exception as e:
            print(e.__class__.__name__)
else:
    print('NO PARAMS')
