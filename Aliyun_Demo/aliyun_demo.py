
import log
import utime
import checkNet
from aLiYun import aLiYun
from usr.Aht20 import Aht20

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_AliYin_example"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


# 设置日志输出级别
log.basicConfig(level=log.INFO)
aliYun_log = log.getLogger("ALiYun")

productKey = "k28gtnnq6qN"  # 产品标识(参照阿里 IoT 平台应用开发指导)
productSecret = None  # 产品密钥（使用一机一密认证时此参数传入None，参照阿里 IoT 平台应用开发指导)
DeviceName = "aliyun_demo"  # 设备名称(参照阿里 IoT 平台应用开发指导)
DeviceSecret = "f9335eaf7e38cce9b82eba1ce5a344be"  # 设备密钥（使用一型一密认证此参数传入None，免预注册暂不支持，需先在 IoT 平台创建设备，参照阿里 IoT 平台应用开发指导)

state = 5

# 回调函数
def sub_cb(topic, msg):
    global state
    aliYun_log.info("Subscribe Recv: Msg={}".format(msg.decode()))
    state -= 1


if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        aliYun_log.info('Network connection successful!')
        # 创建aliyun连接对象
        ali = aLiYun(productKey, productSecret, DeviceName, DeviceSecret)

        # 设置mqtt连接属性
        clientID = "lot_test"  # 自定义字符（不超过64）
        ali.setMqtt(clientID, clean_session=False, keepAlive=300)

        # 设置回调函数
        ali.setCallback(sub_cb)
        topic = "/k28gtnnq6qN/aliyun_demo/user/get"  # IoT 平台自定义或自拥有的Topic
        topic1='/sys/k28gtnnq6qN/aliyun_demo/thing/event/property/post'
        # 订阅主题
        ali.subscribe(topic)
        # 发布消息
        ali.publish(topic,"")
        # 运行
        ali.start()

        while 1:
            if state:
                pass
            else:
                ali.disconnect()
                break
    else:
        aliYun_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))

