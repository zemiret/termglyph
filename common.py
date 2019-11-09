def chars(*args):
    for a in args:
        for i in range(ord(a[0]), ord(a[1]) + 1):
            yield chr(i)

