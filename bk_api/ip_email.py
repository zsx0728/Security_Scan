from bk_api_list_hosts_without_biz import bk_api_list_hosts_without_biz
from bk_api_list_users import bk_api_list_users

def ip_email(ip_file):
  #根据IP，得到IP与username对应的文件
  with open(ip_file) as ip_file :
    for ip_line in ip_file:
      ip_line = ip_line.strip('\n')
      bk_api_list_hosts_without_biz(ip_line)

  user_file = '../log/ip_user_api.txt'
  #根据上面生成的文件，得到username与邮箱对应的文件
  with open(user_file) as user_file, open('../log/user_email_api.txt','a+') as user_out:
    for user_line in user_file :
      user_line = user_line.strip('\n')
      #print("username is",user_line.split()[1])
      user_return_value = bk_api_list_users(user_line.split()[1])
      user_out.write(user_line.split()[0] + ' ' + user_return_value + '\n')

ip_email('../log/ip.txt')
