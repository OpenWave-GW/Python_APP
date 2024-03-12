# Name: dso_sns.py
#
# Description: 
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

"""This module can send some message to SNS"""
import os
import sys
import time
import socket
if sys.implementation.name == "micropython":
    import urequests as requests
    import ubinascii as binascii
    import uhashlib as hashlib
    import ussl as ssl
else:
    import requests
    import binascii
    import hashlib
    import ssl

class LineNotify():
    """This can send Line Notify.

    .. important:: Need to have your own token, https://notify-bot.line.me/en/

    .. important:: Need configure your network DNS settings.

    **Useage:**

    .. code-block:: python

        import dso_sns
        TOKEN = <your tiken>
        l = dso_sns.LineNotify(TOKEN)
        data = l.make_data('Message')
        l.sned(data)

    """
    def __init__(self, token:str=None) -> None:
        if token == None:
            raise Exception('Need token!')
        if sys.implementation.name == "micropython":
            self.__micropython = True
        else:
            self.__micropython = False
        self.token = token

    def make_data(self, msg:str,stickerPackageId:int=None,stickerId:int=None,imageFile:str=None,imageThumbnail:str=None,imageFullsize:str=None) -> dict:
        """This can prepare your data

        Args:
            msg (str): The message you want to send, it's necessarily.
            stickerPackageId (int, optional): The sticker package ID.
            
                Defaults to None.

            stickerId (int, optional): The sticker ID.
            
                Defaults to None.

            imageFile (str, optional): The local image path.
            
                 Defaults to None.
            imageThumbnail (str, optional): The HTTP image URL.

                Defaults to None.
            imageFullsize (str, optional): The HTTP image URL. 
            
                Defaults to None.

        Returns:
            dict: data
        
        .. tip:: The sticker info is here https://developers.line.biz/en/docs/messaging-api/sticker-list/#specify-sticker-in-message-object
        .. note:: If you specified imageThumbnail ,imageFullsize and imageFile, imageFile takes precedence.
        """
        data={}
        if(len(msg)>0):
            data["message"]=msg
        else:
            print("message is empty.")
            return None

        # sticker
        if stickerPackageId == None or stickerId == None:
            pass
        else:
            data["stickerPackageId"]=str(stickerPackageId)
            data["stickerId"]=str(stickerId)

        # imageFile
        if imageFile == None:
            pass
        else:
            data["imageFile"]=imageFile
        
        # imageurl
        if imageThumbnail == None or imageFullsize == None:
            pass
        else:
            data["imageThumbnail"]=imageThumbnail
            data["imageFullsize"]=imageFullsize
        #print(data)
        return data

    def __make_request(self,data:dict):
        boundary = binascii.hexlify(os.urandom(16)).decode('ascii')

        def encode_field(field_name:str):
            if self.__micropython:
                return (
                    b'--%s' % boundary,
                    b'Content-Disposition: form-data; name="%s"' % field_name,
                    b'', 
                    b'%s'% data[field_name]
                )
            else:
                return (
                    b'--%s' % boundary.encode(),
                    b'Content-Disposition: form-data; name="%s"' % field_name.encode(),
                    b'', 
                    b'%s'% data[field_name].encode()
                )

        def encode_file(field_name:str):
            file_full=data[field_name]
            if ".png" in file_full.lower():
                fext = "png"
            elif (".jpg" or ".jpeg") in file_full.lower():
                fext = "jpeg"
            else:
                return ""
            file_name="test."+fext
            with open(file_full,"rb") as fp:
                image=fp.read()
            if self.__micropython:
                return (
                    b'--%s' % boundary,
                    b'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                        field_name, file_name),
                    b'Content-Type: image/%s'%(fext),
                    b'', 
                    image
                )
            else:
                return (
                    b'--%s' % boundary.encode(),
                    b'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                        field_name.encode(), file_name.encode()),
                    b'Content-Type: image/%s'%(fext.encode()),
                    b'', 
                    image
                )

        lines = []
        for name in data:
            if(name == "imageFile"):
                lines.extend(encode_file(name))
            else:
                lines.extend(encode_field(name))
                
        if self.__micropython:
            lines.extend((b'--%s--' % boundary, b''))
        else:
            lines.extend((b'--%s--' % boundary.encode(), b''))
        body = b'\r\n'.join(lines)

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'content-type': 'multipart/form-data; boundary=' + boundary,
            }
        return body, headers

    def send(self, data:dict):
        """Send your data to Line Notify

        Args:
            data (dict): data
        """
        if data == None:
            return
        body, headers=self.__make_request(data)
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, data = body)
        #print(r.text)

class __Twitter():
    """This can tweet.

    .. important:: Need to have your own keys.

    .. important:: Need configure your network DNS settings.

    **Useage:**

    .. code-block:: python

        import dso_sns

        CK = <CONSUMER_KEY>
        CS = <CONSUMER_SECRET>
        AT = <ACCESS_KEY>
        AS = <ACCESS_SECRET>

        t = dso_sns.Twitter(CK,CS,AT,AS)
        t.set_time_zone(8)
        t.send("You can't send same tweet as last time.")
    """
    def __init__(self, CK:str, CS:str, AT:str, AS:str) -> None:
        self.CK = CK #CONSUMER_KEY
        self.CS = CS #CONSUMER_SECRET
        self.AT = AT #ACCESS_KEY
        self.AS = AS #ACCESS_SECRET
        if sys.implementation.name == "micropython":
            self.__micropython = True
            self.tz = 0
        else:
            self.__micropython = False
            self.tz = 0

    def __current_time(self):
        t = int(time.time())
        return t + self.tz *3600

    def __enc_percent(self, s):
        ret = ''
        for c in s:
            ordc = ord(c)
            if ordc in range(0x30, 0x39 + 1) or \
            ordc in range(0x41, 0x5a + 1) or \
            ordc in range(0x61, 0x7a + 1) or \
            ordc in (0x2d, 0x2e, 0x5f, 0x7e):
                ret += c
            else:
                ret += '%%%02X' % (ordc)
        return ret

    def __oauth_sign(self, method, url, s, vcs, vas):
        str = ''
        for t in sorted(s):
            if str != '':
                str += '&'
            str += "%s=%s" % (t[0], self.__enc_percent(t[1]))
        str = "%s&%s&%s" % (method.upper(), self.__enc_percent(url), self.__enc_percent(str))
        if self.__micropython:
            signing_key = bytearray(self.__enc_percent(vcs) + '&' + self.__enc_percent(vas))
        else:
            signing_key = bytearray(self.__enc_percent(vcs).encode() + '&'.encode() + self.__enc_percent(vas).encode())
        try:
            import hmac
            if self.__micropython:
                hash = hmac.new(signing_key, msg=str, digestmod=hashlib.sha1)
            else:
                hash = hmac.new(signing_key, msg=str.encode(), digestmod=hashlib.sha1)
            ret = binascii.b2a_base64(hash.digest()).rstrip()
        except ImportError as e:
            # HMAC implementation, as hashlib/hmac wouldn't fit
            # From https://en.wikipedia.org/wiki/Hash-based_message_authentication_code
            def HMAC_sha1(k, m):
                SHA1 = hashlib.sha1
                SHA1_BLOCK_SIZE = 64
                if(len(k)>SHA1_BLOCK_SIZE):
                    k=SHA1(k).digest()
                KEY_BLOCK = k + (b'\0' * (SHA1_BLOCK_SIZE - len(k)))
                KEY_INNER = bytes((x ^ 0x36) for x in KEY_BLOCK)
                KEY_OUTER = bytes((x ^ 0x5C) for x in KEY_BLOCK)
                inner_message = KEY_INNER + m
                outer_message = KEY_OUTER + SHA1(inner_message).digest()
                return SHA1(outer_message)
            hash=HMAC_sha1(signing_key, str).digest()
            ret = binascii.b2a_base64(hash).rstrip()
        return ret

    def __oauth_genhead(self, vck, vcs, vat, vas, status):
        tstamp = self.__current_time()
        #print('----tstamp----', tstamp)
        nonce = 'nonce%d' % (tstamp)
        pairs = {
            ('status', status),
            ('include_entities', 'true'),
            ('oauth_consumer_key', vck),
            ('oauth_nonce', nonce),
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_timestamp', str(tstamp)),
            ('oauth_token', vat),
            ('oauth_version', '1.0')}

        sig = self.__oauth_sign('POST', \
            'https://api.twitter.com/1.1/statuses/update.json', \
            pairs, vcs, vas).decode('utf-8')
        s = '''    OAuth oauth_consumer_key="%s",
        oauth_nonce="%s",
        oauth_signature="%s",
        oauth_signature_method="HMAC-SHA1",
        oauth_timestamp="%d",
        oauth_token="%s",
        oauth_version="1.0"''' % \
            (vck, nonce, self.__enc_percent(sig), tstamp, vat)
        return s

    def __tweet(self, msg):
        body = 'status=%s' % (self.__enc_percent(msg))
        oauth_head = self.__oauth_genhead(self.CK, self.CS, self.AT, self.AS, msg)
        header = '''POST /1.1/statuses/update.json?include_entities=true HTTP/1.1
Accept: */*
Connection: close
User-Agent: OAuth gem v0.4.4
Content-Type: application/x-www-form-urlencoded
Authorization:
%s
Content-Length: %d
Host: api.twitter.com
''' % (oauth_head, len(body))
        return header + '\n' + body + '\n'

    def send(self, msg:str):
        """Send a message tweet.

        .. caution:: You can't send same tweet as last time.

        Args:
            msg (str): message
        """
        data = self.__tweet(msg)  # Generate data that we are goint to post.
        #print('---Generated data---', data)
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
        addr = socket.getaddrinfo("api.twitter.com", 443)[0][-1]
        s.connect(addr)
        s=ssl.wrap_socket(s)
        if self.__micropython:
            s.write(data)
        else:
            s.write(data.encode())
        #print(s.read(4096))
        s.close()

    def set_time_zone(self,tz:int):
        """Set time zone

        .. hint:: If you are using CPython, you can ignore it.

        Args:
            tz (int): time zone
        """
        if self.__micropython:
            self.tz = tz
        else:
            self.tz = 0

    def get_time_zone(self) -> int:
        """Get time zone

        Returns:
            int: time zone
        """
        return self.tz