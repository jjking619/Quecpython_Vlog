from machine import LCD
import lvgl as lv

# 初始化数据
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
    0, 0, 0x21
)

display_on_data = (
    0, 0, 0x28,
    2, 0, 120,
    0, 0, 0x10,
)

display_off_data = (
    0, 0, 0x11,
    2, 0, 20,
    0, 0, 0x29,
)

def initialize_lcd():
    # 设置 LCD 初始化数据
    lcd = LCD()
    init_list = bytearray(init_data)
    display_on_list = bytearray(display_on_data)
    display_off_list = bytearray(display_off_data)
    invalid_data = bytearray()

    # 初始化 LCD
    lcd.lcd_init(
        init_list,
        240,  # 宽度
        240,  # 高度
        52000,  # 时钟
        1,  # 数据宽度
        4,  # 数据线数
        0,  # 内部电阻
        invalid_data,
        display_on_list,
        display_off_list,
        None
    )

    # 初始化 LVGL 显示驱动
    disp_buf1 = lv.disp_draw_buf_t()
    buf1_1 = bytearray(240 * 240 * 2)
    disp_buf1.init(buf1_1, None, len(buf1_1))
    disp_drv = lv.disp_drv_t()
    disp_drv.init()
    disp_drv.draw_buf = disp_buf1
    disp_drv.flush_cb = lcd.lcd_write
    disp_drv.hor_res = 240
    disp_drv.ver_res = 240
    disp_drv.register()

    # 初始化 LVGL
    lv.init()

    return lcd

# 导出 init_lcd 函数
__all__ = ["initialize_lcd"]
