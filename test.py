def range_practice(start, stop, step, ending=' '):
    for i in range(start, stop + 1, step):
        if i % step == 0:
            print(i, end=ending)
