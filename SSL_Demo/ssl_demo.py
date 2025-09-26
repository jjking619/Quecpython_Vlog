# 导入ussl模块
# -*- coding: UTF-8 -*-
import ussl
import usocket
import log
import utime
import checkNet

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Socket_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
socket_log = log.getLogger("SOCKET")

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        socket_log.info('Network connection successful!')
        # 1. 单向认证说明
        # 创建一个socket实例
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        # 解析域名
        sockaddr=usocket.getaddrinfo('myssl.com', 443)[0][-1]
        # 建立连接
        sock.connect(sockaddr)
        # SSL连接. 前提需要服务器支持
        sock = ussl.wrap_socket(sock, server_hostname="101.37.104.185:41534")
        # 向服务端发送消息
        ret = sock.write('GET / HTTP/1.0\r\nHost: myssl.com\r\nAccept-Encoding: deflate\r\n\r\n')
        socket_log.info('write %d bytes' % ret)
        #接收服务端消息
        data=sock.read(256)
        socket_log.info('read %s bytes:' % len(data))
        print("RECV FROM SERVER:",data.decode())

        # 关闭连接
        sock.close()
        socket_log.info('--------------------Socket Ussl End-------------------')
    else:
        socket_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))

# 2. 双向认证说明
# cert = "数据证书"
# key = "私钥"
# sock = ussl.wrap_socket(sock, server_hostname="myssl.com", cert=cert, key=key)

