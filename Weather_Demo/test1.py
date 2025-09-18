# 检查特定字体是否存在
def check_font(font_name):
    try:
        font = getattr(lv, font_name)
        print("{font_name} 存在")
        return True
    except AttributeError:
        print("{font_name} 不存在")
        return False

# 检查一些常见字体
check_font("font_simsun_18")
check_font("font_unscii_8")
check_font("font_dejavu_16")
check_font("font_simsun_16_cjk")  # 检查中文字体
check_font("font_montserrat_14")