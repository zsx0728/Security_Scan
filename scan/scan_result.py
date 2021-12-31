import os
import fnmatch
import time
import configparser

cf = configparser.ConfigParser(allow_no_value=True)
cf.read('config.ini')
def is_file_match(filename, patterns):
  for pattern in patterns:
    if fnmatch.fnmatch(filename, pattern):
      return True
  return False

def find_specific_files(root, patterns=['*'], exclude_dirs=[]):
  for root, dirnames, filenames in os.walk(root):
    for filename in filenames:
      if is_file_match(filename, patterns):
        yield os.path.join(root, filename)
    for d in exclude_dirs:
      if d in dirnames:
        dirnames.remove(d)

def compare_files(file1, file2, portStat):
  with open(file1) as inf1, open(file2) as inf2, open(cf.get('Basic','ResultFile'), 'a+') as outf :
    content2 = inf2.readlines(-1)
    for line in inf1:
      if line not in content2:
        line = line.strip('\n')
        outf.write(line + ' ' + portStat + '\n')
        outf.flush()
  inf1.close()
  inf2.close()
  outf.close()

def scan_result():
  #找到/var/log/scan目录及子目录下最新的2个文件
  files = {name: os.path.getmtime(name) for name in find_specific_files(cf.get('Basic','LogDir'))}
  result = sorted(files.items(), key=lambda d: d[1], reverse=True)[:2]
  file_new = result[0][0]
  file_old = result[1][0]
  compare_files(file_new, file_old, 'Open')
  compare_files(file_old, file_new, 'Close')
