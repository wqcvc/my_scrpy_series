# # import threading
# # # import time
# # #
# # #
# # # def test_thread(n, a=[]):
# # #     print(f"task {n}")
# # #     time.sleep(1)
# # #     print(f"{n} sleep 1s")
# # #     time.sleep(2)
# # #     print(f"{n} sleep 2s")
# # #     time.sleep(3)
# # #     print(f"{n} sleep 3s")
# # #     print(f"list is:{a}")
# # #
# # #
# # # if __name__ == "__main__":
# # #     listA = [1, 2, 3]
# # #     listB = [6, 7, 8]
# # #     t1 = threading.Thread(target=test_thread, args=("t1", listA))
# # #     t2 = threading.Thread(target=test_thread, args=("t2", listB))
# # #
# # #     t1.setDaemon(True)
# # #     t1.start()
# # #     t2.start()
# # #
# # #     # t1.setName()
# # #     t1.getName()
# # #
# # #     t1.join(timeout=10)
# # #     t2.join(timeout=10)
#
#
# # !/usr/bin/env python3
# # -*- coding: utf-8 -*-
# import requests, threading, datetime
# from bs4 import BeautifulSoup
# import random
#
# import requests
# import  time
# from fake_useragent import UserAgent
#
# my_proxies={'http':'113.194.29.106:9999'}
# my_proxies2={'http':'113.194.29.106:9999'}
# my_proxies3={'http':'111.222.141.127:8118'}
#
# list_prxy=[{},{},{}]
#
# ua = UserAgent()
# headers = {
#     'User-Agent': ua.random,
# }  #
#
# # res=requests.get(url="http://icanhazip.com",proxies=my_proxies3,timeout=7)
# # res2=requests.get(url="http://icanhazip.com",proxies={'http':'113.194.29.106:9999'},headers=headers,timeout=10)
# # res2=requests.get(url="http://httpbin.org/ip",proxies={'http':'113.194.29.106:9999'},timeout=10)
# # res2=requests.get(url="http://api.ipify.org ",proxies={'http':'113.194.29.106:9999'},timeout=10)
# # res2=requests.get(url="https://www.baidu.com",proxies={'https':'171.12.115.181:9999'},timeout=10)
#
#
# # print(res.text)
# # print(res2.status_code)
#
# # try:
# #     requests.get('http://wenshu.court.gov.cn/', proxies={"http":"125.108.99.41:9000"},timeout=7)
# # except:
# #     print('connect failed')
# # else:
# #     print('success')
#
# import execjs
#
# sts=["db9f3zGBuJeUkMOCe6IJqWvFw+crnNiD3k3lQ3ILC3KyOlmDzp1j0FqkxjbsZT6dFbEtjMbYGNze/Haq0gjf1jdqleCr49jtU45cse3NI5jL8R1Y6oBdTwbFdkLjl9Cl075OUmP2TrmByeqOHtxI4vtGxhYdqII1QouazXk38U3tFkglYwey5M0WF5r0yvhp8tk6UoIi5nb8ierpl3f1T98cZzavPrrSjaYYYEG7axw+dZJleQpa/s03BZWxfLcY6Z3ORGe2GzY",
#      "Mix3EFciDSgvGScvCCACei8EIXoVHzdwO1JaGDQjOy5/AVgUMnccNQ9eBQ8tP1UyGChwWn0/SRE3PgEEFBBvESQ6BEQ6fixpFxY0VHwMDShSClM0ZT0qIiEyKwRmVSBFA3J0VyoJdiMTX1sndgZVMlU3ABcOHAowMgEoWiJsKwFmXHt+NwMeezEnOy8gCTc3BTAiHFUbEHIcPzEuPAw9AwcrLFA3ACV5ai95JCc9IR0PLzMVV351ICV9NGksRi4EXTA+RBhdPQB4XSxwJCBDCT57IwQDUkhVPksNMgM2MCUlJCEQDXURcDMWLWEvahAEMWEYKnwaU1QmEjsPPBhTN1I3XyQIEF1EJSIYUi5DUg4=",
#      "bd9f3zGBuJeUkMOCe6IJqWvFw+crnNiD3k3lQ3ILC3KyOlmDzp1j0FqkxjbsZT6dFbEtjMbYGNze/Haq0gjf1jdqleCr49jtU45cse3NI5jL8R1Y6oBdTwbFdkLjl9Cl075OUmP2TrmByeqOHtxI4vtGxhYdqII1QouazXk38U3tFkglYwey5M0WF5r0yvhp8tk6UoIi5nb8ierpl3f1T98cZzavPrrSjaYYYEG7axw+dZJleQpa/s03BZWxfLcY6Z3ORGe2GzY2"]
#
# import  os
# os.environ["EXECJS_RUNTIME"] = "phantomjs"
# def js_exec(strencode: list):
#     """
#     调用js解密：pyexcejs库功能
#     :param strencode: 实际解密参数
#     :return:
#     """
#     print(f"run environ: {execjs.get().name}")
#     # # 1. read js file
#     # with open("strencode.js") as f:
#     #     js_code = f.read()
#     # # 2. compile js func
#     # ctx = execjs.compile(js_code)
#     js="""
#     ;var encode_version = 'jsjiami.com.v5', bxqrm = '__0x99c1f',  __0x99c1f=['PsOMcMOTVQ==','wpHDoSE3fA==','GsO6wpDDsMOZS8O8JMKmw6hcEcOF','ecOYw4TCvDY=','wotowqbDi3I=','BcKewocQwqjCkw==','w4zCqELDj8O8','wpzDgCPDgsO1MFrCmcO5Ly3CrA==','AyoSw450JcK4dQ3Cnw==','WndFTcOR','w5bCtFxgwqE=','VsKfY8KMQg==','DsKgw4VRaiw=','b29sVcO+','w4jCpAk=','w5xEwpgaHQ==','f39tUMOt','wrzDtxoTfjLDsFDDpMKOw5PCncKTNQ==','LsKewrg6wr8=','5YmI6Zim54mJ5pyU5Y6077yye0Lkv6zlr6zmnL/lvpnnqaM=','XcKEJsO7w4w=','woPCix19w5/CisK9w6TDgkVOEcO0','LsKkw7XDgFA=','worDhcOswownVg==','aWfCpjPCjQ==','wrMcc8KoV8KQ','ARABw4R+','OcKWw6HDo1w=','Y3xJSMOo','L1zCojrCrQ==','JsOiw7/CrDfCgQEdwrnClMKYZQ==','CsKTwogFwp/ClGnCmcKrw4M=','JQ9q','NcO+w7TCpBLCgA4Kwp4=','54ue5pyr5Y+v77ypw4LDteS8r+Wvg+afgeW9muepne+9t+i/m+iso+aXueaNpuaIguS6meeauOW1t+S9rg==','M0oq','5YiL6Zui54us5p6g5Yyc77y7wqAr5L6J5ayO5p2z5b2U56mh','woHDpcO2wrA/','w5Biw74YwpM=','BzVx','S21TR8OQ','dHdnRcON','w5zCrEbDpcObwpHChcOHw4DCgHR7dgY=','w5XCh17DqMOS'];(function(_0x20326f,_0x20880f){var _0x564cb8=function(_0x4e7d5f){while(--_0x4e7d5f){_0x20326f['push'](_0x20326f['shift']());}};_0x564cb8(++_0x20880f);}(__0x99c1f,0x1a1));var _0x5e77=function(_0x231fd0,_0x4f680a){_0x231fd0=_0x231fd0-0x0;var _0x5b4826=__0x99c1f[_0x231fd0];if(_0x5e77['initialized']===undefined){(function(){var _0x550fbc=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x18d5c9='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0x550fbc['atob']||(_0x550fbc['atob']=function(_0x4ce2f1){var _0x333808=String(_0x4ce2f1)['replace'](/=+$/,'');for(var _0x432180=0x0,_0x2ab90b,_0x991246,_0x981158=0x0,_0x57b080='';_0x991246=_0x333808['charAt'](_0x981158++);~_0x991246&&(_0x2ab90b=_0x432180%0x4?_0x2ab90b*0x40+_0x991246:_0x991246,_0x432180++%0x4)?_0x57b080+=String['fromCharCode'](0xff&_0x2ab90b>>(-0x2*_0x432180&0x6)):0x0){_0x991246=_0x18d5c9['indexOf'](_0x991246);}return _0x57b080;});}());var _0x219af0=function(_0x441e3a,_0x2cc193){var _0x5f41ea=[],_0x503809=0x0,_0xe42b77,_0x56465b='',_0x52cace='';_0x441e3a=atob(_0x441e3a);for(var _0x39753a=0x0,_0xf81284=_0x441e3a['length'];_0x39753a<_0xf81284;_0x39753a++){_0x52cace+='%'+('00'+_0x441e3a['charCodeAt'](_0x39753a)['toString'](0x10))['slice'](-0x2);}_0x441e3a=decodeURIComponent(_0x52cace);for(var _0x307b3e=0x0;_0x307b3e<0x100;_0x307b3e++){_0x5f41ea[_0x307b3e]=_0x307b3e;}for(_0x307b3e=0x0;_0x307b3e<0x100;_0x307b3e++){_0x503809=(_0x503809+_0x5f41ea[_0x307b3e]+_0x2cc193['charCodeAt'](_0x307b3e%_0x2cc193['length']))%0x100;_0xe42b77=_0x5f41ea[_0x307b3e];_0x5f41ea[_0x307b3e]=_0x5f41ea[_0x503809];_0x5f41ea[_0x503809]=_0xe42b77;}_0x307b3e=0x0;_0x503809=0x0;for(var _0x3ab53f=0x0;_0x3ab53f<_0x441e3a['length'];_0x3ab53f++){_0x307b3e=(_0x307b3e+0x1)%0x100;_0x503809=(_0x503809+_0x5f41ea[_0x307b3e])%0x100;_0xe42b77=_0x5f41ea[_0x307b3e];_0x5f41ea[_0x307b3e]=_0x5f41ea[_0x503809];_0x5f41ea[_0x503809]=_0xe42b77;_0x56465b+=String['fromCharCode'](_0x441e3a['charCodeAt'](_0x3ab53f)^_0x5f41ea[(_0x5f41ea[_0x307b3e]+_0x5f41ea[_0x503809])%0x100]);}return _0x56465b;};_0x5e77['rc4']=_0x219af0;_0x5e77['data']={};_0x5e77['initialized']=!![];}var _0xfeb75b=_0x5e77['data'][_0x231fd0];if(_0xfeb75b===undefined){if(_0x5e77['once']===undefined){_0x5e77['once']=!![];}_0x5b4826=_0x5e77['rc4'](_0x5b4826,_0x4f680a);_0x5e77['data'][_0x231fd0]=_0x5b4826;}else{_0x5b4826=_0xfeb75b;}return _0x5b4826;};function strencode(_0x67dc43,_0x4a4e2c,_0x4b0d50){var _0x518445={'rUJzL':_0x5e77('0x0','l6Io'),'aRrxI':function _0x49676a(_0x1630be,_0x13bc8a){return _0x1630be(_0x13bc8a);},'dBxJx':function _0x5cfff4(_0x464ec4,_0x475764){return _0x464ec4==_0x475764;},'zfcNo':function _0x1aca76(_0x4f2cfe,_0x2e2fc3){return _0x4f2cfe<_0x2e2fc3;},'NqIoV':function _0xc1f9d6(_0x375348,_0x1d4824){return _0x375348%_0x1d4824;}};var _0x5913a9=_0x518445['rUJzL'][_0x5e77('0x1','(CgI')]('|'),_0x9727ce=0x0;while(!![]){switch(_0x5913a9[_0x9727ce++]){case'0':l=_0x4b0d50[_0x5e77('0x2','1K^x')](-0x1);continue;case'1':return _0x518445[_0x5e77('0x3','gRb5')](atob,code);case'2':len=_0x4a4e2c[_0x5e77('0x4','S8ez')];continue;case'3':_0x67dc43=_0x518445[_0x5e77('0x5','ymN[')](atob,_0x67dc43);continue;case'4':if(_0x518445[_0x5e77('0x6','(CgI')](l,0x2)){t=_0x67dc43;_0x67dc43=_0x4a4e2c;_0x4a4e2c=t;}continue;case'5':for(i=0x0;_0x518445[_0x5e77('0x7','J1vC')](i,_0x67dc43['length']);i++){k=_0x518445[_0x5e77('0x8','N3$4')](i,len);code+=String[_0x5e77('0x9','9mT#')](_0x67dc43['charCodeAt'](i)^_0x4a4e2c[_0x5e77('0xa','JIFn')](k));}continue;case'6':code='';continue;}break;}};(function(_0x3982b5,_0x5ef47c,_0x2a610c){var _0x1d682c={'xUxOl':function _0x22faa8(_0x125424,_0x317215){return _0x125424===_0x317215;},'ayTEY':_0x5e77('0xb','c1Q!'),'RwyAW':_0x5e77('0xc','9mT#'),'mmMCJ':function _0x325c3b(_0x4c9902,_0x36525b){return _0x4c9902===_0x36525b;},'cXrdh':'LBn','GeQMc':_0x5e77('0xd','ewfs'),'QpglS':function _0x4b476d(_0x131d26,_0xad2d5f){return _0x131d26<_0xad2d5f;},'zwnCF':function _0x42746f(_0x15381f,_0x134c72){return _0x15381f%_0x134c72;},'CmoKV':function _0x4c7855(_0x2714ea,_0x1950a1){return _0x2714ea(_0x1950a1);},'eCuaM':function _0x3d5ae8(_0x701d58,_0x10016a){return _0x701d58(_0x10016a);},'hjyBM':function _0x1b06bb(_0x19252a,_0x36e3de){return _0x19252a==_0x36e3de;},'cVtTM':function _0x2eb18c(_0x4db8e4,_0x30834b){return _0x4db8e4!==_0x30834b;},'vuFSy':_0x5e77('0xe','!JaV'),'feGVj':function _0x2c9926(_0x4f6385,_0x5267d8){return _0x4f6385===_0x5267d8;},'QTNTV':_0x5e77('0xf','8I#[')};_0x2a610c='al';try{if(_0x1d682c[_0x5e77('0x10','1K^x')](_0x1d682c[_0x5e77('0x11','$V0W')],'UYY')){t=input;input=key;key=t;}else{_0x2a610c+=_0x5e77('0x12','c1Q!');_0x5ef47c=encode_version;if(!(typeof _0x5ef47c!==_0x1d682c[_0x5e77('0x13','J1vC')]&&_0x1d682c[_0x5e77('0x14','J1vC')](_0x5ef47c,_0x5e77('0x15','Owl6')))){if(_0x1d682c[_0x5e77('0x16','Owl6')]===_0x1d682c[_0x5e77('0x17','kZq4')]){_0x3982b5[_0x2a610c]('ɾ��'+_0x1d682c[_0x5e77('0x18','Tx$c')]);}else{var _0x6bef38=_0x5e77('0x19','8I#[')[_0x5e77('0x1a','2qLA')]('|'),_0x2acb41=0x0;while(!![]){switch(_0x6bef38[_0x2acb41++]){case'0':for(i=0x0;_0x1d682c[_0x5e77('0x1b','aqTc')](i,input[_0x5e77('0x1c','JIFn')]);i++){k=_0x1d682c[_0x5e77('0x1d','Owl6')](i,len);code+=String[_0x5e77('0x1e','5JYb')](input[_0x5e77('0x1f','ymN[')](i)^key['charCodeAt'](k));}continue;case'1':l=fuck['substr'](-0x1);continue;case'2':input=_0x1d682c[_0x5e77('0x20','J1vC')](atob,input);continue;case'3':return _0x1d682c[_0x5e77('0x21','l6Io')](atob,code);case'4':if(_0x1d682c[_0x5e77('0x22','&6&I')](l,0x2)){t=input;input=key;key=t;}continue;case'5':code='';continue;case'6':len=key[_0x5e77('0x23','9D[4')];continue;}break;}}}}}catch(_0x109b3f){if(_0x1d682c['cVtTM'](_0x1d682c[_0x5e77('0x24','J1vC')],_0x1d682c['vuFSy'])){_0x2a610c='al';try{_0x2a610c+=_0x5e77('0x25','X@)x');_0x5ef47c=encode_version;if(!(_0x1d682c['cVtTM'](typeof _0x5ef47c,_0x1d682c[_0x5e77('0x26','X7%n')])&&_0x1d682c[_0x5e77('0x27','J1vC')](_0x5ef47c,_0x5e77('0x28','Tx$c')))){_0x3982b5[_0x2a610c]('ɾ��'+_0x1d682c[_0x5e77('0x29','JIFn')]);}}catch(_0x5948fd){_0x3982b5[_0x2a610c](_0x5e77('0x2a','B&JQ'));}}else{_0x3982b5[_0x2a610c](_0x1d682c[_0x5e77('0x2b','g5#$')]);}}}(window));;encode_version = 'jsjiami.com.v5';
#     """
#
#     ctx = execjs.compile(js)
#     # 3. call js func
#     print("3")
#     # ctx.call('strencode', strencode[0], strencode[1])
#     # encodes = re.findall('strencode\("(.*?)","(.*?)"', content)[0]
#     ctx.call('strencode', 'db9f3zGBuJeUkMOCe6IJqWvFw+crnNiD3k3lQ3ILC3KyOlmDzp1j0FqkxjbsZT6dFbEtjMbYGNze/Haq0gjf1jdqleCr49jtU45cse3NI5jL8R1Y6oBdTwbFdkLjl9Cl075OUmP2TrmByeqOHtxI4vtGxhYdqII1QouazXk38U3tFkglYwey5M0WF5r0yvhp8tk6UoIi5nb8ierpl3f1T98cZzavPrrSjaYYYEG7axw+dZJleQpa/s03BZWxfLcY6Z3ORGe2GzY', 'Mix3EFciDSgvGScvCCACei8EIXoVHzdwO1JaGDQjOy5/AVgUMnccNQ9eBQ8tP1UyGChwWn0/SRE3PgEEFBBvESQ6BEQ6fixpFxY0VHwMDShSClM0ZT0qIiEyKwRmVSBFA3J0VyoJdiMTX1sndgZVMlU3ABcOHAowMgEoWiJsKwFmXHt+NwMeezEnOy8gCTc3BTAiHFUbEHIcPzEuPAw9AwcrLFA3ACV5ai95JCc9IR0PLzMVV351ICV9NGksRi4EXTA+RBhdPQB4XSxwJCBDCT57IwQDUkhVPksNMgM2MCUlJCEQDXURcDMWLWEvahAEMWEYKnwaU1QmEjsPPBhTN1I3XyQIEF1EJSIYUi5DUg4=')
#
# # js_exec(sts)
#
#
# import logging
#
# logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
# logger=logging.getLogger()
#
# logger.info(f"?????")
#
#
# from pyppeteer import launch
# import asyncio
# import asyncio
# from pyppeteer import launch
# import time
#
#
# async def main():
#     start=time.time()
#     launch_args = {
#         "headless": True,  # 关闭无头浏览器
#         "args": [
#             "--start-maximized",
#             "--no-sandbox",
#             "--disable-infobars",
#             "--ignore-certificate-errors",
#             "--log-level=3",
#             "--enable-extensions",
#             "--window-size=1920,1080",
#             #"--refer=https://0722.91p51.com/video.php?category=rf&page=1",
#             "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
#         ],
#     }
#     browser = await launch(**launch_args)
#     page = await browser.newPage()
#     res=await page.goto(
#         # 'https://0722.91p51.com/view_video.php?viewkey=5f1ce5096ebc088204d5&page=1&viewtype=basic&category=rf',timeout=60000)  # 跳转
#         'https://www.baidu.com',options={'timeout': 30000})  # 跳转
#     await page.screenshot({'path': 'example.png'})  # 截图
#
#     res.text()
#     page.title()
#     page.content()
#     page.cookies()
#
#
#     print(await page.content())
#     # dimensions = await page.evaluate('document.write(strencode("9d806mYY9cYo7oWqKCrILLKHOS+fFbBXCabDhAGK0/NfD6ALbTWDbdE3JSmdqNqE3G6D7Ai+CdGjjPE1bwhQ7m6G/vvYQmEu9+d49O3Ng6FKV/HLUV+W94+oKYp0PffPULwNxi3WAWChd9VW4mn/TEkk4LuMlUt8O31MwUI7+eKahSXGYg/Sc7kMKUuVNvY3JqyiLKgwqV46pRTB2mcHWnZ6L5x82hTwz7iWOYUx281x+Uf3THSAIYi+4/1Lxu5A42BfH0mMhCA","aSx2RlI1EzNjMBsVVAIaSAFxGnkoBAp+AyoSDBwPEDIPCwk8CwUSMnxCABAmZXk6AAwWdC8dfUkFBwpUPwoWMFEfd3RncicbEzIvOz5gMUQAGlk4ZTlSK2MgMBEdOjIMd0c2fW8IUCM9XHcmGGsCJwM6fWNtcEMlKmtBAgQPEjo2fBh8LgAKZhJldgAyYToSUF00azAAPR9RJyMINT5NYS1dVQAjExt4cj0NFCcHGiY7Ih8lLWBSHxINPwQDDB90HTQ3HSgDIUMiOm5XKj8OKmFfWj8BAwsEGGALSmQ9bTQeBAovAg86CmBvUk1JHSR4Dg4BNCogCkxQZ107IiEFL1BfLg0SZ1U7ChsACS5CBAs=","9d806mYY9cYo7oWqKCårILLKHOS+fFbBXCabDhAGK0/NfD6ALbTWDbdE3JSmdqNqE3G6D7Ai+CdGjjPE1bwhQ7m6G/vvYQmEu9+d49O3Ng6FKV/HLUV+W94+oKYp0PffPULwNxi3WAWChd9VW4mn/TEkk4LuMlUt8O31MwUI7+eKahSXGYg/Sc7kMKUuVNvY3JqyiLKgwqV46pRTB2mcHWnZ6L5x82hTwz7iWOYUx281x+Uf3THSAIYi+4/1Lxu5A42BfH0mMhCA2"));')
#     #
#     # print(dimensions)
#
#
#     await browser.close()  # 关闭
#
#     end=time.time()
#     # import threading
#     # # import time
#     # #
#     # #
#     # # def test_thread(n, a=[]):
#     # #     print(f"task {n}")
#     # #     time.sleep(1)
#     # #     print(f"{n} sleep 1s")
#     # #     time.sleep(2)
#     # #     print(f"{n} sleep 2s")
#     # #     time.sleep(3)
#     # #     print(f"{n} sleep 3s")
#     # #     print(f"list is:{a}")
#     # #
#     # #
#     # # if __name__ == "__main__":
#     # #     listA = [1, 2, 3]
#     # #     listB = [6, 7, 8]
#     # #     t1 = threading.Thread(target=test_thread, args=("t1", listA))
#     # #     t2 = threading.Thread(target=test_thread, args=("t2", listB))
#     # #
#     # #     t1.setDaemon(True)
#     # #     t1.start()
#     # #     t2.start()
#     # #
#     # #     # t1.setName()
#     # #     t1.getName()
#     # #
#     # #     t1.join(timeout=10)
#     # #     t2.join(timeout=10)
#
#     # !/usr/bin/env python3
#     # -*- coding: utf-8 -*-
#     import requests, threading, datetime
#     from bs4 import BeautifulSoup
#     import random
#
#     import requests
#     from fake_useragent import UserAgent
#
#     my_proxies = {'http': '113.194.29.106:9999'}
#     my_proxies2 = {'http': '113.194.29.106:9999'}
#     my_proxies3 = {'http': '111.222.141.127:8118'}
#
#     list_prxy = [{}, {}, {}]
#
#     ua = UserAgent()
#     headers = {
#         'User-Agent': ua.random,
#     }  #
#
#     # res=requests.get(url="http://icanhazip.com",proxies=my_proxies3,timeout=7)
#     # res2=requests.get(url="http://icanhazip.com",proxies={'http':'113.194.29.106:9999'},headers=headers,timeout=10)
#     # res2=requests.get(url="http://httpbin.org/ip",proxies={'http':'113.194.29.106:9999'},timeout=10)
#     # res2=requests.get(url="http://api.ipify.org ",proxies={'http':'113.194.29.106:9999'},timeout=10)
#     # res2=requests.get(url="https://www.baidu.com",proxies={'https':'171.12.115.181:9999'},timeout=10)
#
#     # print(res.text)
#     # print(res2.status_code)
#
#     # try:
#     #     requests.get('http://wenshu.court.gov.cn/', proxies={"http":"125.108.99.41:9000"},timeout=7)
#     # except:
#     #     print('connect failed')
#     # else:
#     #     print('success')
#
#     import execjs
#
#     sts = [
#         "db9f3zGBuJeUkMOCe6IJqWvFw+crnNiD3k3lQ3ILC3KyOlmDzp1j0FqkxjbsZT6dFbEtjMbYGNze/Haq0gjf1jdqleCr49jtU45cse3NI5jL8R1Y6oBdTwbFdkLjl9Cl075OUmP2TrmByeqOHtxI4vtGxhYdqII1QouazXk38U3tFkglYwey5M0WF5r0yvhp8tk6UoIi5nb8ierpl3f1T98cZzavPrrSjaYYYEG7axw+dZJleQpa/s03BZWxfLcY6Z3ORGe2GzY",
#         "Mix3EFciDSgvGScvCCACei8EIXoVHzdwO1JaGDQjOy5/AVgUMnccNQ9eBQ8tP1UyGChwWn0/SRE3PgEEFBBvESQ6BEQ6fixpFxY0VHwMDShSClM0ZT0qIiEyKwRmVSBFA3J0VyoJdiMTX1sndgZVMlU3ABcOHAowMgEoWiJsKwFmXHt+NwMeezEnOy8gCTc3BTAiHFUbEHIcPzEuPAw9AwcrLFA3ACV5ai95JCc9IR0PLzMVV351ICV9NGksRi4EXTA+RBhdPQB4XSxwJCBDCT57IwQDUkhVPksNMgM2MCUlJCEQDXURcDMWLWEvahAEMWEYKnwaU1QmEjsPPBhTN1I3XyQIEF1EJSIYUi5DUg4=",
#         "bd9f3zGBuJeUkMOCe6IJqWvFw+crnNiD3k3lQ3ILC3KyOlmDzp1j0FqkxjbsZT6dFbEtjMbYGNze/Haq0gjf1jdqleCr49jtU45cse3NI5jL8R1Y6oBdTwbFdkLjl9Cl075OUmP2TrmByeqOHtxI4vtGxhYdqII1QouazXk38U3tFkglYwey5M0WF5r0yvhp8tk6UoIi5nb8ierpl3f1T98cZzavPrrSjaYYYEG7axw+dZJleQpa/s03BZWxfLcY6Z3ORGe2GzY2"]
#
#     import os
#     os.environ["EXECJS_RUNTIME"] = "phantomjs"
#
#     def js_exec(strencode: list):
#         """
#         调用js解密：pyexcejs库功能
#         :param strencode: 实际解密参数
#         :return:
#         """
#         print(f"run environ: {execjs.get().name}")
#         # # 1. read js file
#         # with open("strencode.js") as f:
#         #     js_code = f.read()
#         # # 2. compile js func
#         # ctx = execjs.compile(js_code)
#         js = """
#         ;var encode_version = 'jsjiami.com.v5', bxqrm = '__0x99c1f',  __0x99c1f=['PsOMcMOTVQ==','wpHDoSE3fA==','GsO6wpDDsMOZS8O8JMKmw6hcEcOF','ecOYw4TCvDY=','wotowqbDi3I=','BcKewocQwqjCkw==','w4zCqELDj8O8','wpzDgCPDgsO1MFrCmcO5Ly3CrA==','AyoSw450JcK4dQ3Cnw==','WndFTcOR','w5bCtFxgwqE=','VsKfY8KMQg==','DsKgw4VRaiw=','b29sVcO+','w4jCpAk=','w5xEwpgaHQ==','f39tUMOt','wrzDtxoTfjLDsFDDpMKOw5PCncKTNQ==','LsKewrg6wr8=','5YmI6Zim54mJ5pyU5Y6077yye0Lkv6zlr6zmnL/lvpnnqaM=','XcKEJsO7w4w=','woPCix19w5/CisK9w6TDgkVOEcO0','LsKkw7XDgFA=','worDhcOswownVg==','aWfCpjPCjQ==','wrMcc8KoV8KQ','ARABw4R+','OcKWw6HDo1w=','Y3xJSMOo','L1zCojrCrQ==','JsOiw7/CrDfCgQEdwrnClMKYZQ==','CsKTwogFwp/ClGnCmcKrw4M=','JQ9q','NcO+w7TCpBLCgA4Kwp4=','54ue5pyr5Y+v77ypw4LDteS8r+Wvg+afgeW9muepne+9t+i/m+iso+aXueaNpuaIguS6meeauOW1t+S9rg==','M0oq','5YiL6Zui54us5p6g5Yyc77y7wqAr5L6J5ayO5p2z5b2U56mh','woHDpcO2wrA/','w5Biw74YwpM=','BzVx','S21TR8OQ','dHdnRcON','w5zCrEbDpcObwpHChcOHw4DCgHR7dgY=','w5XCh17DqMOS'];(function(_0x20326f,_0x20880f){var _0x564cb8=function(_0x4e7d5f){while(--_0x4e7d5f){_0x20326f['push'](_0x20326f['shift']());}};_0x564cb8(++_0x20880f);}(__0x99c1f,0x1a1));var _0x5e77=function(_0x231fd0,_0x4f680a){_0x231fd0=_0x231fd0-0x0;var _0x5b4826=__0x99c1f[_0x231fd0];if(_0x5e77['initialized']===undefined){(function(){var _0x550fbc=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x18d5c9='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0x550fbc['atob']||(_0x550fbc['atob']=function(_0x4ce2f1){var _0x333808=String(_0x4ce2f1)['replace'](/=+$/,'');for(var _0x432180=0x0,_0x2ab90b,_0x991246,_0x981158=0x0,_0x57b080='';_0x991246=_0x333808['charAt'](_0x981158++);~_0x991246&&(_0x2ab90b=_0x432180%0x4?_0x2ab90b*0x40+_0x991246:_0x991246,_0x432180++%0x4)?_0x57b080+=String['fromCharCode'](0xff&_0x2ab90b>>(-0x2*_0x432180&0x6)):0x0){_0x991246=_0x18d5c9['indexOf'](_0x991246);}return _0x57b080;});}());var _0x219af0=function(_0x441e3a,_0x2cc193){var _0x5f41ea=[],_0x503809=0x0,_0xe42b77,_0x56465b='',_0x52cace='';_0x441e3a=atob(_0x441e3a);for(var _0x39753a=0x0,_0xf81284=_0x441e3a['length'];_0x39753a<_0xf81284;_0x39753a++){_0x52cace+='%'+('00'+_0x441e3a['charCodeAt'](_0x39753a)['toString'](0x10))['slice'](-0x2);}_0x441e3a=decodeURIComponent(_0x52cace);for(var _0x307b3e=0x0;_0x307b3e<0x100;_0x307b3e++){_0x5f41ea[_0x307b3e]=_0x307b3e;}for(_0x307b3e=0x0;_0x307b3e<0x100;_0x307b3e++){_0x503809=(_0x503809+_0x5f41ea[_0x307b3e]+_0x2cc193['charCodeAt'](_0x307b3e%_0x2cc193['length']))%0x100;_0xe42b77=_0x5f41ea[_0x307b3e];_0x5f41ea[_0x307b3e]=_0x5f41ea[_0x503809];_0x5f41ea[_0x503809]=_0xe42b77;}_0x307b3e=0x0;_0x503809=0x0;for(var _0x3ab53f=0x0;_0x3ab53f<_0x441e3a['length'];_0x3ab53f++){_0x307b3e=(_0x307b3e+0x1)%0x100;_0x503809=(_0x503809+_0x5f41ea[_0x307b3e])%0x100;_0xe42b77=_0x5f41ea[_0x307b3e];_0x5f41ea[_0x307b3e]=_0x5f41ea[_0x503809];_0x5f41ea[_0x503809]=_0xe42b77;_0x56465b+=String['fromCharCode'](_0x441e3a['charCodeAt'](_0x3ab53f)^_0x5f41ea[(_0x5f41ea[_0x307b3e]+_0x5f41ea[_0x503809])%0x100]);}return _0x56465b;};_0x5e77['rc4']=_0x219af0;_0x5e77['data']={};_0x5e77['initialized']=!![];}var _0xfeb75b=_0x5e77['data'][_0x231fd0];if(_0xfeb75b===undefined){if(_0x5e77['once']===undefined){_0x5e77['once']=!![];}_0x5b4826=_0x5e77['rc4'](_0x5b4826,_0x4f680a);_0x5e77['data'][_0x231fd0]=_0x5b4826;}else{_0x5b4826=_0xfeb75b;}return _0x5b4826;};function strencode(_0x67dc43,_0x4a4e2c,_0x4b0d50){var _0x518445={'rUJzL':_0x5e77('0x0','l6Io'),'aRrxI':function _0x49676a(_0x1630be,_0x13bc8a){return _0x1630be(_0x13bc8a);},'dBxJx':function _0x5cfff4(_0x464ec4,_0x475764){return _0x464ec4==_0x475764;},'zfcNo':function _0x1aca76(_0x4f2cfe,_0x2e2fc3){return _0x4f2cfe<_0x2e2fc3;},'NqIoV':function _0xc1f9d6(_0x375348,_0x1d4824){return _0x375348%_0x1d4824;}};var _0x5913a9=_0x518445['rUJzL'][_0x5e77('0x1','(CgI')]('|'),_0x9727ce=0x0;while(!![]){switch(_0x5913a9[_0x9727ce++]){case'0':l=_0x4b0d50[_0x5e77('0x2','1K^x')](-0x1);continue;case'1':return _0x518445[_0x5e77('0x3','gRb5')](atob,code);case'2':len=_0x4a4e2c[_0x5e77('0x4','S8ez')];continue;case'3':_0x67dc43=_0x518445[_0x5e77('0x5','ymN[')](atob,_0x67dc43);continue;case'4':if(_0x518445[_0x5e77('0x6','(CgI')](l,0x2)){t=_0x67dc43;_0x67dc43=_0x4a4e2c;_0x4a4e2c=t;}continue;case'5':for(i=0x0;_0x518445[_0x5e77('0x7','J1vC')](i,_0x67dc43['length']);i++){k=_0x518445[_0x5e77('0x8','N3$4')](i,len);code+=String[_0x5e77('0x9','9mT#')](_0x67dc43['charCodeAt'](i)^_0x4a4e2c[_0x5e77('0xa','JIFn')](k));}continue;case'6':code='';continue;}break;}};(function(_0x3982b5,_0x5ef47c,_0x2a610c){var _0x1d682c={'xUxOl':function _0x22faa8(_0x125424,_0x317215){return _0x125424===_0x317215;},'ayTEY':_0x5e77('0xb','c1Q!'),'RwyAW':_0x5e77('0xc','9mT#'),'mmMCJ':function _0x325c3b(_0x4c9902,_0x36525b){return _0x4c9902===_0x36525b;},'cXrdh':'LBn','GeQMc':_0x5e77('0xd','ewfs'),'QpglS':function _0x4b476d(_0x131d26,_0xad2d5f){return _0x131d26<_0xad2d5f;},'zwnCF':function _0x42746f(_0x15381f,_0x134c72){return _0x15381f%_0x134c72;},'CmoKV':function _0x4c7855(_0x2714ea,_0x1950a1){return _0x2714ea(_0x1950a1);},'eCuaM':function _0x3d5ae8(_0x701d58,_0x10016a){return _0x701d58(_0x10016a);},'hjyBM':function _0x1b06bb(_0x19252a,_0x36e3de){return _0x19252a==_0x36e3de;},'cVtTM':function _0x2eb18c(_0x4db8e4,_0x30834b){return _0x4db8e4!==_0x30834b;},'vuFSy':_0x5e77('0xe','!JaV'),'feGVj':function _0x2c9926(_0x4f6385,_0x5267d8){return _0x4f6385===_0x5267d8;},'QTNTV':_0x5e77('0xf','8I#[')};_0x2a610c='al';try{if(_0x1d682c[_0x5e77('0x10','1K^x')](_0x1d682c[_0x5e77('0x11','$V0W')],'UYY')){t=input;input=key;key=t;}else{_0x2a610c+=_0x5e77('0x12','c1Q!');_0x5ef47c=encode_version;if(!(typeof _0x5ef47c!==_0x1d682c[_0x5e77('0x13','J1vC')]&&_0x1d682c[_0x5e77('0x14','J1vC')](_0x5ef47c,_0x5e77('0x15','Owl6')))){if(_0x1d682c[_0x5e77('0x16','Owl6')]===_0x1d682c[_0x5e77('0x17','kZq4')]){_0x3982b5[_0x2a610c]('ɾ��'+_0x1d682c[_0x5e77('0x18','Tx$c')]);}else{var _0x6bef38=_0x5e77('0x19','8I#[')[_0x5e77('0x1a','2qLA')]('|'),_0x2acb41=0x0;while(!![]){switch(_0x6bef38[_0x2acb41++]){case'0':for(i=0x0;_0x1d682c[_0x5e77('0x1b','aqTc')](i,input[_0x5e77('0x1c','JIFn')]);i++){k=_0x1d682c[_0x5e77('0x1d','Owl6')](i,len);code+=String[_0x5e77('0x1e','5JYb')](input[_0x5e77('0x1f','ymN[')](i)^key['charCodeAt'](k));}continue;case'1':l=fuck['substr'](-0x1);continue;case'2':input=_0x1d682c[_0x5e77('0x20','J1vC')](atob,input);continue;case'3':return _0x1d682c[_0x5e77('0x21','l6Io')](atob,code);case'4':if(_0x1d682c[_0x5e77('0x22','&6&I')](l,0x2)){t=input;input=key;key=t;}continue;case'5':code='';continue;case'6':len=key[_0x5e77('0x23','9D[4')];continue;}break;}}}}}catch(_0x109b3f){if(_0x1d682c['cVtTM'](_0x1d682c[_0x5e77('0x24','J1vC')],_0x1d682c['vuFSy'])){_0x2a610c='al';try{_0x2a610c+=_0x5e77('0x25','X@)x');_0x5ef47c=encode_version;if(!(_0x1d682c['cVtTM'](typeof _0x5ef47c,_0x1d682c[_0x5e77('0x26','X7%n')])&&_0x1d682c[_0x5e77('0x27','J1vC')](_0x5ef47c,_0x5e77('0x28','Tx$c')))){_0x3982b5[_0x2a610c]('ɾ��'+_0x1d682c[_0x5e77('0x29','JIFn')]);}}catch(_0x5948fd){_0x3982b5[_0x2a610c](_0x5e77('0x2a','B&JQ'));}}else{_0x3982b5[_0x2a610c](_0x1d682c[_0x5e77('0x2b','g5#$')]);}}}(window));;encode_version = 'jsjiami.com.v5';
#         """
#
#         ctx = execjs.compile(js)
#         # 3. call js func
#         print("3")
#         # ctx.call('strencode', strencode[0], strencode[1])
#         # encodes = re.findall('strencode\("(.*?)","(.*?)"', content)[0]
#         ctx.call('strencode',
#                  'db9f3zGBuJeUkMOCe6IJqWvFw+crnNiD3k3lQ3ILC3KyOlmDzp1j0FqkxjbsZT6dFbEtjMbYGNze/Haq0gjf1jdqleCr49jtU45cse3NI5jL8R1Y6oBdTwbFdkLjl9Cl075OUmP2TrmByeqOHtxI4vtGxhYdqII1QouazXk38U3tFkglYwey5M0WF5r0yvhp8tk6UoIi5nb8ierpl3f1T98cZzavPrrSjaYYYEG7axw+dZJleQpa/s03BZWxfLcY6Z3ORGe2GzY',
#                  'Mix3EFciDSgvGScvCCACei8EIXoVHzdwO1JaGDQjOy5/AVgUMnccNQ9eBQ8tP1UyGChwWn0/SRE3PgEEFBBvESQ6BEQ6fixpFxY0VHwMDShSClM0ZT0qIiEyKwRmVSBFA3J0VyoJdiMTX1sndgZVMlU3ABcOHAowMgEoWiJsKwFmXHt+NwMeezEnOy8gCTc3BTAiHFUbEHIcPzEuPAw9AwcrLFA3ACV5ai95JCc9IR0PLzMVV351ICV9NGksRi4EXTA+RBhdPQB4XSxwJCBDCT57IwQDUkhVPksNMgM2MCUlJCEQDXURcDMWLWEvahAEMWEYKnwaU1QmEjsPPBhTN1I3XyQIEF1EJSIYUi5DUg4=')
#
#     # js_exec(sts)
#
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

logger.info(f"?????")

from pyppeteer import launch
import asyncio
import asyncio
from pyppeteer import launch
import time
import re

async def main():
    start = time.time()
    launch_args = {
        "headless": True,  # 关闭无头浏览器
        "dumpio": True,
        "args": [
            "--start-maximized",
            "--no-sandbox",
            "--disable-infobars",
            "--ignore-certificate-errors",
            "--log-level=3",
            "--enable-extensions",
            "--window-size=1920,1080",
            "--refer=https://0722.91p51.com/video.php?category=rf&page=1",
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        ],
    }
    browser = await launch(**launch_args)
    page = await browser.newPage()
    res = await page.goto(
        'https://0722.91p51.com/view_video.php?viewkey=ebaec4277896006083f7&page=1&viewtype=basic&category=rf',timeout=360000)  # 跳转
        # 'https://www.baidu.com', options={'timeout': 30000})  # 跳转
    await page.screenshot({'path': 'example.png'})  # 截图

    res.text()
    page.title()
    page.content()
    page.cookies()

    print(await page.content())
    # dimensions = await page.evaluate('document.write(strencode("9d806mYY9cYo7oWqKCrILLKHOS+fFbBXCabDhAGK0/NfD6ALbTWDbdE3JSmdqNqE3G6D7Ai+CdGjjPE1bwhQ7m6G/vvYQmEu9+d49O3Ng6FKV/HLUV+W94+oKYp0PffPULwNxi3WAWChd9VW4mn/TEkk4LuMlUt8O31MwUI7+eKahSXGYg/Sc7kMKUuVNvY3JqyiLKgwqV46pRTB2mcHWnZ6L5x82hTwz7iWOYUx281x+Uf3THSAIYi+4/1Lxu5A42BfH0mMhCA","aSx2RlI1EzNjMBsVVAIaSAFxGnkoBAp+AyoSDBwPEDIPCwk8CwUSMnxCABAmZXk6AAwWdC8dfUkFBwpUPwoWMFEfd3RncicbEzIvOz5gMUQAGlk4ZTlSK2MgMBEdOjIMd0c2fW8IUCM9XHcmGGsCJwM6fWNtcEMlKmtBAgQPEjo2fBh8LgAKZhJldgAyYToSUF00azAAPR9RJyMINT5NYS1dVQAjExt4cj0NFCcHGiY7Ih8lLWBSHxINPwQDDB90HTQ3HSgDIUMiOm5XKj8OKmFfWj8BAwsEGGALSmQ9bTQeBAovAg86CmBvUk1JHSR4Dg4BNCogCkxQZ107IiEFL1BfLg0SZ1U7ChsACS5CBAs=","9d806mYY9cYo7oWqKCårILLKHOS+fFbBXCabDhAGK0/NfD6ALbTWDbdE3JSmdqNqE3G6D7Ai+CdGjjPE1bwhQ7m6G/vvYQmEu9+d49O3Ng6FKV/HLUV+W94+oKYp0PffPULwNxi3WAWChd9VW4mn/TEkk4LuMlUt8O31MwUI7+eKahSXGYg/Sc7kMKUuVNvY3JqyiLKgwqV46pRTB2mcHWnZ6L5x82hTwz7iWOYUx281x+Uf3THSAIYi+4/1Lxu5A42BfH0mMhCA2"));')
    #
    # print(dimensions)
    #  </script><source src="http://cfdc.91p52.com//mp43/398448.mp4?st=6Ta5l-nsLaLzyTZ-yCqXGQ&amp;f=3b26v3jC54hMPtndpdcyh05/AuOKuhPemII6Umr52vsXuwE2iZJcnkgLEAKsT5PNBHVH2ALPBQDURu9EmJmaE6DRCXlnAFS2IHUw+Jo" type="video/mp4">
    url_re = re.findall('http.?://.*.91p\d{2}.com/.?mp43/.*.mp4\\?.*=.*f=[^"]*', str(await page.content()))
    tittle = re.findall(r'<h4 class="login_register_header" align=left>(.*?)</h4>', str(await page.content()), re.S)
    img_url = re.findall(r'poster="(.*?)"', str(await page.content()))

    await browser.close()  # 关闭

    end = time.time()

    print(f"total run seconds: [{end - start}]")
    return url_re,tittle,img_url
#
# s1,s2,s3=asyncio.get_event_loop().run_until_complete(main())
# print(f"ssss is :{s1,s2,s3}")
# from fake_useragent import  UserAgent
#
# ua=UserAgent()
# print(f"\"--user-agent={ua.random}\"")

import  re
str="""https://img2.t6k.co/thumb/399042.jpg" preload="auto" class="video-js vjs-sublime-skin vjs-16-9 vjs-paused player_one-dimensions vjs-workinghover vjs-v7 vjs-user-active vjs-error vjs-controls-disabled" id="player_one" tabindex="-1" lang="en-us" role="region" aria-label="Video Player" style="visibility: visible;"><video id="player_one_html5_api" class="vjs-tech" preload="auto" poster="https://img2.t6k.co/thumb/399042.jpg" data-setup="{}" tabindex="-1" src="https://cfdc.91p52.com//mp43/399042.mp4?st=c812BSP58uMPGq0pIm4PRw&amp;f=4f77LAv/WNUGF2Obxoo0zbqWt/T6KB/x7ysBtve3eAFw+7QvChJmHOZRspwxmM5sxTy4QWfWrDqVaF/4rioVajoE/qH/wF/vrZPQ2w"""
str2="""https://ccn.91p52.com//mp43/399037.mp4?st=WGDUdhJH_yxw0RO4kg_fxw&amp;f=5367IaGnenGddK7hp1KY3qA80lfhSkKKX6ixx6W9IHOh8R8ee8E6Y98nIGIkx5r5FWoBXoU6jNXQoNVzSnvdDGgCUaOasC0BfKdc9Q"""
str3="""<div data-setup="{}" poster="https://img2.t6k.co/thumb/399083.jpg" preload="auto" class="video-js vjs-sublime-skin vjs-16-9 vjs-paused player_one-dimensions vjs-controls-enabled vjs-workinghover vjs-v7 vjs-user-active" id="player_one" tabindex="-1" lang="en-us" role="region" aria-label="Video Player" style="visibility: visible;"><video id="player_one_html5_api" class="vjs-tech" preload="auto" poster="https://img2.t6k.co/thumb/399083.jpg" data-setup="{}" tabindex="-1">"""

tittle = re.findall(r'poster="(.*?)"', str3)
# tittle = re.findall("http.?://.*.91p.*.com/.?mp43/.*.mp4", str)

print(tittle)

dict2222={'2020-10-15':['1.234','2.3333'],'2020-10-14':['3.455','6.789']}

for k,v in dict2222.items():
    print(k,v[0],v[1])

url='xxx ddd vvv'

r_url_1=url.replace('xxx','sss').replace('ddd','fff').replace('vvv','lll')
print(r_url_1)