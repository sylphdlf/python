
import linecache
import os

filename = '/Users/lfd/Documents/workspace.nosync/log/webApi_err.log'
# print(linecache.getline(filename, 2))
# print(len(linecache.getlines(filename)))
# print(os.path.getsize(filename))
f = open(filename, 'r')
print(f.seek(0, 2))
f.seek(14956,0)
print(f.read(22434-14956))

f.close()