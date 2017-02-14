import os
from fnmatch import fnmatch

#Add root directory
root = '<<root directory>>'
#search for a pattern
pattern = "*.java"

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            file = os.path.join(path,name)
            absfile = file.replace('\\','/') #to get windows specific path
            print absfile
            f=open(absfile,'a')
            f.write('\n'+"//REVIEW") # can write string to files
            f.close()
