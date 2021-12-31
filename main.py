from scan.nmap_scan import nmap_scan
from scan.scan_result import scan_result
from email.send_mail import send_mail
import os
import configparser

cf = configparser.ConfigParser(allow_no_value=True)
cf.read('config.ini')
def main():
  #扫描指定网段的端口，扫描结果写入日志，日志文件以程序执行时间命名，类似202112201557.txt
  nmap_scan()

  print("The number of logfile is/are %s" % len(os.listdir(cf.get('Basic','LogDir'))))
  #如果日志文件夹中只有1个日志文件，证明为初次使用，不进行新旧日志的对比，不发送对比结果；如果日志数量大于1，进行新旧日志对比，并将对比结果写入邮件并发送
  if len(os.listdir(cf.get('Basic','LogDir'))) > 1:
    #将最近生成的2个日志文件进行对比，将新增的开放/关闭端口写入对比文件
    scan_result()
    #通过邮件发送对比文件给指定用户
    send_mail()

if __name__ == '__main__':
    main()
