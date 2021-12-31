import requests
import json
import configparser

# 得到主机IP与维护者姓名,将结果写入文件:ip_user_api.txt
def bk_api_list_hosts_without_biz(host_ip):
  #如果API的ip_url是https的，需要添加该行，忽略密钥认证引发的告警
  requests.packages.urllib3.disable_warnings()
  #蓝鲸API的URL
  ip_url = "https://xxx/api/c/compapi/v2/cc/list_hosts_without_biz/"
  #API参数
  ip_data = {
    "bk_app_code" : "bk_user_manage",
    "bk_app_secret" : "xxx",
    "bk_username" : "admin",
    "page": {
      "start": 0,
      "limit": 30
      },
    "fields": [
          "bk_host_id",
          "bk_cloud_id",
          "bk_host_innerip",
          "bk_os_type",
          "operator"
      ],
    # host_property_filter参数使用说明：https://github.com/Tencent/bk-cmdb/blob/master/src/common/querybuilder/README.md
    "host_property_filter": {
      "condition": "AND",
      "rules": [
              {
                  "field": "bk_host_innerip",
                  "operator": "equal",
                  "value": host_ip
                  #"operator": "begins_with",
                  #"value": "192.168"
              }
        ]
      }
  }
  #发送post请求，接收返回值
  r_ip = requests.post(url=ip_url, data=json.dumps(ip_data), verify=False)
  #将返回值转换为json格式
  response_ip_dict = r_ip.json()
  ip_dicts = response_ip_dict['data']
  demo_ip_dict = ip_dicts['info']
  print("ip number is ",len(demo_ip_dict))
  #将返回值中的bk_host_innerip（IP）和operator（维护人）写入文件
  with open('../log/ip_user_api.txt','a+') as ip_out:
    for ip_number in range(len(demo_ip_dict)):
      ip_out.write(demo_ip_dict[ip_number]['bk_host_innerip'] + ' ' + demo_ip_dict[ip_number]['operator'] + '\n')
      ip_out.flush()
  ip_out.close()
