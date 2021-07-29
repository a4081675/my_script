# coding: utf-8
'''
@author: sy-records
@license: https://github.com/sy-records/v-checkin/blob/master/LICENSE
@contact: 52o@qq52o.cn
@desc: 腾讯视频好莱坞会员V力值签到，支持两次签到：一次正常签到，一次手机签到。
@blog: https://qq52o.me
'''

import sys
import importlib
importlib.reload(sys)
import requests

auth_refresh_url = 'https://access.video.qq.com/user/auth_refresh?vappid=11059694&vsecret=fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe&type=qq&g_tk=&g_vstk=2023974134&g_actk=1689968561&callback=jQuery19109866335862860551_1627529325498&_=1627529325499'
sckey = ''

push_url = "http://www.pushplus.plus/send"
push_token = 'd19b4748f5284e08b3bcf02b44db8686'
push_topic = '1'
url1 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2'

urls=[
    'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=7&_=1582364733058&callback=Zepto1582364712694',#下载签到请求
    'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=6&_=1582366326994&callback=Zepto1582366310545',#签到请求
    'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2&_=1555060502385&callback=Zepto1555060502385',#赠送签到请求
    'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=3&_=1582368319252&callback=Zepto1582368297765',#弹幕签到请求
    'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=1&_=1582997048625&callback=Zepto1582997031843'#观看60分钟签到
]
url2 = 'https://v.qq.com/x/bu/mobile_checkin'

login_headers = {
    'Referer': 'https://v.qq.com',
    'Cookie': 'RK=CAbQJFCKe4; ptcz=c9fb68098ff093b537c2739ad13f15dd2a3faf37ad1fefec82b42dedef27550e; pgv_pvid=3135694488; video_platform=2; video_guid=d4898ff042fdc1ac; o_cookie=569516648; pac_uid=1_569516648; tvfe_boss_uuid=05cc7ec915c88f7f; _ga=GA1.2.1493900977.1626316588; pgv_info=ssid=s3098279818; _qpsvr_localtk=0.4951937116946292; main_login=qq; vqq_access_token=8AF2ACC845F30212717DD91BF52B86CB; vqq_appid=101483052; vqq_openid=D4908F8B488055EE25A43C41B76BECE1; vqq_vuserid=129027891; vqq_vusession=8MISsQhwuww2oom6GwXiUg..; vqq_refresh_token=D36B1BBBDB437A23DF362C2B1F4CB953; login_time_init=2021-7-29 11:27:58; uid=94413229; vqq_next_refresh_time=6595; vqq_login_time_init=1627529282; '
}

login = requests.get(auth_refresh_url, headers=login_headers)
cookie = requests.utils.dict_from_cookiejar(login.cookies)
status = "签到通知：\n"

if not cookie:
    print("auth_refresh error")
    payload = {'token':push_token,'topic':push_topic,'title': '腾讯视频V力值签到通知', 'content': '获取Cookie失败，Cookie失效'}
    requests.post(push_url, params=payload)

sign_headers = {
    'Cookie': 'RK=CAbQJFCKe4; ptcz=c9fb68098ff093b537c2739ad13f15dd2a3faf37ad1fefec82b42dedef27550e; pgv_pvid=3135694488; video_platform=2; video_guid=d4898ff042fdc1ac; o_cookie=569516648; pac_uid=1_569516648; tvfe_boss_uuid=05cc7ec915c88f7f; _ga=GA1.2.1493900977.1626316588; pgv_info=ssid=s3098279818; _qpsvr_localtk=0.4951937116946292; main_login=qq; vqq_access_token=8AF2ACC845F30212717DD91BF52B86CB; vqq_appid=101483052; vqq_openid=D4908F8B488055EE25A43C41B76BECE1; vqq_vuserid=129027891; vqq_vusession=8MISsQhwuww2oom6GwXiUg..; vqq_refresh_token=D36B1BBBDB437A23DF362C2B1F4CB953; login_time_init=2021-7-29 11:27:58; uid=94413229; vqq_next_refresh_time=6595; vqq_login_time_init=1627529282; vqq_vusession=' + cookie['vqq_vusession'] + ';',
    'Referer': 'https://m.v.qq.com'
}
def start():
  global status
  for url in urls:
    sign1 = requests.get(url,headers=sign_headers).text
    if 'Account Verify Error' in sign1:
        print('Sign1 error,Cookie Invalid')
        status += "\n\n链接1 失败，Cookie失效"+sign1
    else:
        print('Sign1 Success')
        status += "\n\n链接1 成功，获得V力值：" + sign1[42:-14]

  sign2 = requests.get(url2,headers=sign_headers).text
  if 'Unauthorized' in sign2:
    print('Sign2 error,Cookie Invalid')
    status += "\n\n 链接2 失败，Cookie失效"+sign2
  else:
    print('Sign2 Success')
    status += "\n\n 链接2 成功"

  payload = {'token':push_token,'topic':push_topic,'title': '腾讯视频V力值签到通知', 'content': status}
  push_return=requests.post(push_url, params=payload).text
  print('push_return='+push_return)

def main_handler(event, context):
  return start()
if __name__ == '__main__':
  start()