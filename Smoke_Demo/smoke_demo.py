from machine import Pin
from misc import ADC
import utime
import sms

ps2_y = ADC()
ps2_y.open()

# 循环检测
while True:
    val_y = ps2_y.read(ADC.ADC1)  # 读取ADC值，范围：0-4095
    print("烟雾浓度 (ppm): {:.2f}".format(val_y))
    if   val_y >= 300:
        break
    utime.sleep(1)

sms.deleteMsg(1,4)
sms.sendTextMsg("13558435306","检测到烟雾，请及时处理",'UCS2')
sms.searchTextMsg(0)

