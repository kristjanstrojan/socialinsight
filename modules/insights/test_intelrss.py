from intelrss import RSS
r = RSS("http://inkubator40.si/feed/")
for i in r:
    print(str(i))

