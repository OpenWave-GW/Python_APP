# Name: wechat.py
#
# Description: Push the message or image to the WeChat client.
#
# Author: MK Huang
#
# Documentation:
#   https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import os
import sys
import urequests as req
import ujson as json

cfg = {
    "appid"       :  "", # 測試號 appID
    "appsecret"   :  "", # 測試號 appsecret
    "openid"      :  "", # 關注測試號後的微信號
    "template_id" :  "", # 測試模板的模板ID
}

class WeChat:
    def __init__(self):
        self.read_appid()
        self.token = self.get_access_token()   

    def __str_type_chk(self, line):
        try:
            return int(line)
        except ValueError:
            pass
        try:
            return float(line)
        except ValueError:
            pass
        try:
            return list(map(float, line.split(',')))
        except ValueError:
            d = {"ON": True, "OFF": False}
            return d.get(line.upper(), str(line))

    def loadfile2dict(self, sour, dest):
        try:
            with open(sour,'r') as f:
                for line in f:
                    if line[0] != '#' and len(line.split()) != 0:
                        r = self.__str_type_chk(line.split('=')[1].strip())
                        dest[line.split('=')[0].strip()] = r
        except:
            dso.dsodraw.draw_poptext('Load file error')
            sys.exit()

    def read_appid(self):
        self.loadfile2dict('wechat.txt', cfg)
        self.appid = cfg["appid"]
        self.appsecret = cfg["appsecret"]
        self.openid = cfg["openid"]
        self.template_id = cfg["template_id"]

    def get_access_token(self):
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}"
        response = req.get(url)
        res = response.json()        
        if "access_token" in res:
            token = res["access_token"]
            return token
        else:
            errmsg = res["errmsg"]
            errcode = res["errcode"]
            dso.dsodraw.draw_poptext("Errcode %d: %s!" % (errcode, errmsg))
            sys.exit()

    def send_temple_msg(self):
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={self.token}"
        jData = {
            "touser": self.openid,
            "template_id": self.template_id,    
            "data": {
                "content": {"value": "微信測試"}
            }
        }
        headers = {"Content-type": "application/json"}
        data = json.dumps(jData).encode()
        response = req.post(url=url, data=data, headers=headers)
        res = response.json()
        errcode = res["errcode"]
        errmsg = res["errmsg"]
        if errcode != 0:
            dso.dsodraw.draw_poptext("Errcode %d: %s!" % (errcode, errmsg))
            sys.exit()
        else:
            print("Message sent!")

    def make_request(self, image=None):
        boundary = '---011000010111000001101001' 
        #boundary fixed instead of generating new one everytime
        
        def encode_file(field_name):  # prepares lines for the file
            filename = 'latest.jpg'  # dummy name is assigned to uploaded file
            return (
                b'--%s' % boundary,
                b'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                    field_name, filename),
                b'', 
                image
            )

        lines = [] # empty array initiated
        if image:
            lines.extend(encode_file('photo')) # adding lines  image
        lines.extend((b'--%s--' % boundary, b'')) # ending  with boundary

        body = b'\r\n'.join(lines) # joining all lines constitues body
        body = body + b'\r\n' # extra addtion at the end of file

        headers = {
            'content-type': 'multipart/form-data; boundary=' + boundary
            }  # removed content length parameter
        return body, headers  # body contains the assembled upload package

    def upload_media(self, media_type, media_path):
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={self.token}&type={media_type}"
        buf = open(media_path, 'rb').read()
        data, headers  = self.make_request(buf) # generate body to upload
        response = req.post(url, headers=headers, data=data)
        parse_json = json.loads(response.content.decode())
        return parse_json.get('media_id')
    
    def send_media(self, media_type, media_path):
        media_id = self.upload_media(media_type, media_path)
        url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.token}&type={media_type}"
        if media_type == "image":
            body = {
                "touser": self.openid,
                "msgtype": "image",
                "image":{
                    "media_id": media_id
                }
            }
        data = json.dumps(body)
        response = req.post(url, data=data)
        res = response.json()
        errcode = res["errcode"]
        if errcode == 45015:
            dso.dsodraw.draw_poptext("Errcode 45015: Send message to sandbox account and try again!")
            sys.exit()
        elif errcode != 0:
            dso.dsodraw.draw_poptext("Errcode %d: %s!" % (errcode, errmsg))
            sys.exit()
        else:
            print("Image sent!")

if __name__ == '__main__':
    os.chdir(sys.path[0])
    try:
        import gds_info as gds
    except ImportError:
        import dso2kp as gds
    
    dso = gds.Dso()
    dso.connect()
    dso.dsodraw.draw_poptext('Start Demo')
    we = WeChat()
    we.send_temple_msg()
    we.send_media('image', 'test.png')
    dso.dsodraw.draw_poptext('Complete!')
    dso.close()
    
