from PIL import Image, ImageDraw, ImageFont
import os

# 參數: 圖片檔案、梗圖文字
def create_meme_image(input_image: Image.Image, text: str) -> Image.Image:
    w, h = input_image.size
    border_size = int(w * 0.05)      # 邊框寬度設定為圖片寬度的5%
    margin_bottom = int(h * 0.15)      # 底部保留空間設定為圖片高度的15%
    
    # 計算新的圖片尺寸
    new_width = w + border_size * 2
    new_height = h + border_size * 2 + margin_bottom
    
    # 建立一個黑色背景的新影像
    meme_bg = Image.new("RGB", (new_width, new_height), color=(0, 0, 0))
    meme_bg.paste(input_image, (border_size, border_size))
    
    # 根據圖片寬度動態設定字體大小
    font_size = int(w * 0.075)  # 字體大小為圖片寬度的5%，可以依需求調整
    try:
        font_path = "fonts/NaikaiFont-Light.ttf"
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        elif os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    
    draw = ImageDraw.Draw(meme_bg)
    
    # 使用新方法計算文字尺寸
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_w, text_h = draw.textsize(text, font=font)
    
    # 計算文字置中的位置
    text_x = (new_width - text_w) // 2
    text_y = h + border_size * 2 + (margin_bottom - text_h) // 2

    draw.text((text_x, text_y), text, fill="white", font=font)
    
    return meme_bg

new_img = create_meme_image(Image.open("for-demo-purposes/example.jpg"), "The divine cans of oden.")
new_img.save("for-demo-purposes/meme.jpg")
new_img.show()
