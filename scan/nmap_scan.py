import nmap                       #导入模块
import os
import time
import configparser

def nmap_scan():
  cf = configparser.ConfigParser(allow_no_value=True)
  cf.read('config.ini')

  #创建存储扫描日志的文件夹
  fileDirPath = cf.get('Basic','LogDir') + '/'
  if not os.path.exists(fileDirPath):
      os.makedirs(fileDirPath)
      print('文件夹创建完成  '+fileDirPath)

  #创建扫描日志文件
  time_now = time.strftime("%Y%m%d%H%M", time.localtime())
  fileDir = fileDirPath + time_now + '.txt'
  out = open(fileDir, "a+")

  nm = nmap.PortScanner()           #导入函数
  nm.scan(cf.get('Basic','IPRange'),cf.get('Basic','PortRange')) #输入你要扫描的ip与道口
  for host in nm.all_hosts():       #返回被扫描的主机列表给host
      print('---------------------------------------------------------')
      print('Host : %s (%s)' % (host,nm[host].hostname()))    #nm[host].hostname()获取目标主机的主机名
      print('State : %s' % nm[host].state())                  #nm[host].state()获取主机的状态  |up|down|unknow|skipped|
      for proto in nm[host].all_protocols():                  #nm[host].all_protocols获取执行的协议['tcp','udp']
          print('-----------------------------------------------------')
          print('protocol : %s' % proto )                     #输出执行的协议
          lport = nm[host][proto].keys()                      #获取目标主机所开放的端口赋值给lport
          # lport.sort()
          for port in lport:                                                                  #将lport赋值给port并遍历
              print('port : %s\tstate : %s\tname : %s' % (port,nm[host][proto][port]['state'],nm[host][proto][port]['name']))          #输出扫描结果
              print(host, port, nm[host][proto][port]['name'], sep=" ", file=out)

  out.close()
