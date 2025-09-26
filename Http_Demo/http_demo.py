import request
import utime

url='https://api.apiopen.top/api/sentences'

response = request.get(url)
for i in response.text:
    print(i)
    utime.sleep_ms(10)

# https://api.oick.cn/api/dog?apikey=a4f420d14a0ff3ae18ca7976f0a0f8df