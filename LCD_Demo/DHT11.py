import utime
from machine import Pin

class DHT11:
    def __init__(self, pin_num):
        """
        初始化DHT11传感器 - ASR芯片适配版
        :param pin_num: 引脚编号，例如18
        """
        # ASR芯片可能需要不同的引脚初始化方式
        self.pin = Pin(pin_num, Pin.OUT, Pin.PULL_PU,0)
        self.temperature = None
        self.humidity = None
        # print("DHT11初始化完成，使用引脚: {pin_num}")
        
    def _send_start_signal(self):
        """发送开始信号到DHT11 - ASR适配版"""
        # 设置引脚为输出模式
        self.pin.init(Pin.OUT, Pin.PULL_UP)
        # 拉低至少18ms
        self.pin.value(0)
        utime.sleep_ms(20)
        # 拉高20-40us
        self.pin.value(1)
        utime.sleep_us(30)
        
    def _read_data(self):
        """读取40位数据 - ASR适配版"""
        # 切换为输入模式
        self.pin.init(Pin.IN, Pin.PULL_UP)
        
        data = [0, 0, 0, 0, 0]
        
        # 等待DHT11响应
        # 等待低电平(响应信号)
        timeout = 1000
        while self.pin.value() == 1:
            timeout -= 1
            if timeout == 0:
                return None
            utime.sleep_us(1)
            
        # 等待高电平(响应信号结束)
        timeout = 1000
        while self.pin.value() == 0:
            timeout -= 1
            if timeout == 0:
                return None
            utime.sleep_us(1)
            
        # 等待低电平(准备发送数据)
        timeout = 1000
        while self.pin.value() == 1:
            timeout -= 1
            if timeout == 0:
                return None
            utime.sleep_us(1)
        
        # 读取40位数据
        for i in range(5):
            for j in range(8):
                # 等待高电平开始(数据位开始)
                timeout = 1000
                while self.pin.value() == 0:
                    timeout -= 1
                    if timeout == 0:
                        return None
                    utime.sleep_us(1)
                
                # 测量高电平持续时间
                start = utime.ticks_us()
                timeout = 1000
                while self.pin.value() == 1:
                    timeout -= 1
                    if timeout == 0:
                        return None
                    utime.sleep_us(1)
                
                duration = utime.ticks_diff(utime.ticks_us(), start)
                # 高电平持续时间大于40us表示'1'
                if duration > 40:
                    data[i] |= (1 << (7 - j))
        
        return data
    
    def read(self):
        """读取温湿度数据"""
        try:
            # 发送开始信号
            self._send_start_signal()
            
            # 读取数据
            data = self._read_data()
            if data is None:
                print("读取数据失败")
                return False
                
            # 验证校验和
            checksum = (data[0] + data[1] + data[2] + data[3]) & 0xFF
            if checksum != data[4]:
                print("校验和错误: {checksum} != {data[4]}")
                return False
                
            # 解析数据
            self.humidity = data[0] + data[1] * 0.1
            self.temperature = data[2] + data[3] * 0.1
            
            # 恢复引脚状态
            self.pin.init(Pin.OUT, Pin.PULL_UP)
            self.pin.value(1)
            
            print("读取成功: 温度={self.temperature}, 湿度={self.humidity}")
            return True
            
        except Exception as e:
            print("读取过程中发生异常: {e}")
            return False
    
    def get_temperature(self):
        return self.temperature
    
    def get_humidity(self):
        return self.humidity

# 主程序
def main():
    print("DHT11温湿度传感器测试 - ASR芯片适配版")
    print("====================================")
    
    # 初始化DHT11传感器，使用GPIO18
    dht11 = DHT11(18)  # 使用引脚18
    
    # 尝试读取多次
    for i in range(5):
        print("尝试第 {i+1} 次读取...")
        if dht11.read():
            print("温度: {:.2f}°C, 湿度: {:.2f}%".format(
                dht11.get_temperature(), dht11.get_humidity()))
            break
        else:
            print("读取失败，2秒后重试...")
            utime.sleep(2)
    else:
        print("多次尝试均失败，请检查硬件连接")

# 运行主程序
if __name__ == "__main__":
    main()