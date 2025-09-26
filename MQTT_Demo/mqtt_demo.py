from umqtt import MQTTClient
import utime
import log
import checkNet
'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_MQTT_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
mqtt_log = log.getLogger("MQTT")


state = 0

def sub_cb(topic, msg):
    global state
    mqtt_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
    state = 1


if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        mqtt_log.info('Network connection successful!')

        # 创建一个mqtt实例
        c = MQTTClient("umqtt_client", "broker-cn.emqx.io", 1883)
        # 设置消息回调
        c.set_callback(sub_cb)
        #建立连接
        c.connect()
        # 订阅主题
        c.subscribe(b"/testTopic/kane")
        mqtt_log.info("Connected to broker-cn.emqx.io, subscribed to /testTopic/kane topic" )
        c.publish(b"/testTopic/kane", b"my name is Quecpython!")
        mqtt_log.info("Publish topic: /testTopic/kane, msg: my name is Quecpython")

        while True:
            c.wait_msg()  # 阻塞函数，监听消息
            if state == 1:
                break
        # 关闭连接
        c.disconnect()
    else:
        mqtt_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))

