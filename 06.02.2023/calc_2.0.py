import sys


data = sys.argv[1:]
if data:
    try:
        summ = 0
        for i in range(0, len(data), 2):
            summ += int(data[i])
            if i + 1 < len(data):
                summ -= int(data[i + 1])
    except Exception as e:
        summ = e.__class__.__name__
    finally:
        print(summ)
else:
    print('NO PARAMS')
