from machine import LCD
import lvgl as lv
import time 
import request
import ure
init_data = (
            0, 0, 0x11,
            2, 0, 120,
            0, 1, 0x36,
            1, 1, 0x00,
            0, 1, 0x3A,
            1, 1, 0x05,
            0, 5, 0xB2,
            1, 1, 0x05,
            1, 1, 0x05,
            1, 1, 0x00,
            1, 1, 0x33,
            1, 1, 0x33,
            0, 1, 0xB7,
            1, 1, 0x75,
            0, 1, 0xBB,
            1, 1, 0x22,
            0, 1, 0xC0,
            1, 1, 0x2C,
            0, 1, 0xC2,
            1, 1, 0x01,
            0, 1, 0xC3,
            1, 1, 0x13,
            0, 1, 0xC4,
            1, 1, 0x20,
            0, 1, 0xC6,
            1, 1, 0x11,
            0, 2, 0xD0,
            1, 1, 0xA4,
            1, 1, 0xA1,
            0, 1, 0xD6,
            1, 1, 0xA1,
            0, 14, 0xE0,
            1, 1, 0xD0,
            1, 1, 0x05,
            1, 1, 0x0A,
            1, 1, 0x09,
            1, 1, 0x08,
            1, 1, 0x05,
            1, 1, 0x2E,
            1, 1, 0x44,
            1, 1, 0x45,
            1, 1, 0x0F,
            1, 1, 0x17,
            1, 1, 0x16,
            1, 1, 0x2B,
            1, 1, 0x33,
            0, 14, 0xE1,
            1, 1, 0xD0,
            1, 1, 0x05,
            1, 1, 0x0A,
            1, 1, 0x09,
            1, 1, 0x08,
            1, 1, 0x05,
            1, 1, 0x2E,
            1, 1, 0x43,
            1, 1, 0x45,
            1, 1, 0x0F,
            1, 1, 0x16,
            1, 1, 0x16,
            1, 1, 0x2B,
            1, 1, 0x33,
            0, 0, 0x29,
            0, 0, 0x21)

display_on_data = (
            0, 0, 0x28,
            2, 0, 120,
            0, 0, 0x10,
)
display_off_data =(
            0, 0, 0x11,
            2, 0, 20,
            0, 0, 0x29,
)
# 设置区域参数
XSTART_H = 0xf0
XSTART_L = 0xf1
YSTART_H = 0xf2
YSTART_L = 0xf3
XEND_H = 0xE0
XEND_L = 0xE1
YEND_H = 0xE2
YEND_L = 0xE3
invalid_data = (
    0, 4, 0x2a,
    1, 1, XSTART_H,
    1, 1, XSTART_L,
    1, 1, XEND_H,
    1, 1, XEND_L,
    0, 4, 0x2b,
    1, 1, YSTART_H,
    1, 1, YSTART_L,
    1, 1, YEND_H,
    1, 1, YEND_L,
    0, 0, 0x2c,
)

lcd = LCD()
init_list = bytearray(init_data)
display_on_list = bytearray(display_on_data)
display_off_list = bytearray(display_off_data)
invalid_list = bytearray(invalid_data)
lcd.lcd_init(init_list, 240,320,52000,1,4,0,invalid_list,display_on_list,display_off_list,None)
lv.init()
LCD_SIZE_W = 240
LCD_SIZE_H = 320
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytearray(LCD_SIZE_W * LCD_SIZE_H * 2)


# 城市映射字典

# city_mapping = {
#     'guilin': '桂林',
#     'beijing': '北京',
#     'shanghai': '上海',
#     'guangzhou': '广州',
#     'shenzhen': '深圳',
#     'chongqing': '重庆',
# }
while True:
     # 先清理屏幕

    disp_buf1.init(buf1_1, None, len(buf1_1))
    disp_drv = lv.disp_drv_t()
    disp_drv.init()
    disp_drv.draw_buf = disp_buf1
    disp_drv.flush_cb = lcd.lcd_write
    disp_drv.hor_res = LCD_SIZE_W
    disp_drv.ver_res = LCD_SIZE_H
    disp_drv.register()


    lv.tick_inc(5)
    lv.task_handler()
    screen = lv.obj()


    #显示公司logo
    img1 = lv.img(screen)
    img1.set_pos(0, 20)
    img1.set_src("U:/logo.png")
    city_input = input("请输入城市简称(如guilin): ").strip()
    # 打印原始输入以便调试
    # print("原始输入：", repr(city_input))

    # 尝试从输入中提取城市简称：如果输入中包含冒号，则取冒号后的部分
    if ':' in city_input:
        parts = city_input.split(':')
        city_input = parts[-1].strip()

    # 进一步清洗：只保留字母并转换为小写（假设城市简称都是英文字母）
    clean_input = ''
    for char in city_input:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            clean_input += char
    city_input = clean_input.lower()


    # url = 'http://restapi.amap.com/v3/weather/weatherInfo?key=1336689712e3b12c7c1a6c423a6eed93&city={}&extensions=base'.format(city_chinese)
    url='https://api.seniverse.com/v3/weather/now.json?key=S-YriGgA5ZnYVAJ_G&location={}&language=zh-Hans&unit=c'.format(city_input)
    # print("生成的完整 URL 是：", url)
    
    response = request.get(url)
    data = response.json()
    print(data)
    # weather_data = data["lives"][0]
    # print(weather_data)
     # 提取天气数据
    weather_info = data["results"][0]
    city= weather_info["location"]['name']
    now = weather_info["now"]
    weather_text = now["text"]
    temperature = now["temperature"]
    last_update = weather_info["last_update"]

# 验证 last_update 是否为空或格式不正确
    if not last_update or not isinstance(last_update, str):
        print("last_update 字段为空或格式不正确")
        continue

# 去掉 T 和 + 后边的所有字符，并将 T 替换为空格
    formatted_time = last_update.replace("T", " ").split("+")[0]
    
    # 显示天气信息
    # 创建LVGL显示组件
    label = lv.label(screen)
    label.set_long_mode(lv.label.LONG.WRAP)
    label.set_width(LCD_SIZE_W)

    default_style = lv.style_t()
    default_style.init()

    label.set_text("\n".join([
        "城市 ：{}\n".format(city),          # 城市名称
        "实时天气： {}\n".format(weather_text),  # 天气描述
        "温度： {}℃\n".format(temperature),  # 温度
        "更新时间 :{}\n".format(formatted_time)   # 更新时间
    ]))

    default_style.set_text_font_v2("font_mix.bin",21, 0)
    label.align(lv.ALIGN.TOP_LEFT, 10, 120)
    label.add_style(default_style, lv.PART.MAIN | lv.STATE.DEFAULT)

    lv.scr_load(screen)
