import requests
import json
import configparser

# 得到维护者与邮箱，返回调用结果
def bk_api_list_users(username):
  #如果API的ip_url是https的，需要添加该行，忽略密钥认证引发的告警
  requests.packages.urllib3.disable_warnings()
  #蓝鲸API的URL
  user_url = "https://xxx/api/c/compapi/v2/usermanage/list_users/"
  #API参数
  user_data = {
    "bk_app_code" : "bk_user_manage",
    "bk_app_secret" : "xxx",
    "bk_username" : "admin",
    "lookup_field" : "username",
    "no_page" : True,
    "exact_lookups" : username
  }
  #发送post请求，接收返回值
  r_user = requests.post(url=user_url, data=json.dumps(user_data), verify=False)
  response_user_dict = r_user.json()
  user_dicts = response_user_dict['data']
  #调用API找到结果，执行if部分
  if len(user_dicts) > 0 :
    user_return_value =  user_dicts[0]["username"] + " " + user_dicts[0]["email"]
    print(user_dicts[0]["username"] + " " + user_dicts[0]["email"])
    return user_return_value
  #调用API未找到结果，执行else部分
  else :
    user_return_value = "can't find this username: " + username
    print("can't find this username:", username)
    return user_return_value
