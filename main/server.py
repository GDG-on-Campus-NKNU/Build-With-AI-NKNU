import io, uuid
import os, base64
from fastapi import FastAPI, File, UploadFile, Response
from PIL import Image, ImageDraw, ImageFont, ImageFile
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image as VertexImage

app = FastAPI()

vertexai.init(project=os.getenv('PROJECTID'), location=os.getenv('REGION'))
model = GenerativeModel(model_name="gemini-2.0-flash-001")

# ImageFile.LOAD_TRUNCATED_IMAGES = True

def generate_meme_text(image_data: bytes) -> str:
    """
    呼叫 Gemini Vision，針對該圖片產生一句幽默或有趣的描述。
    目前 Vertex AI SDK 還沒有支援直接 bytes/base64 輸入給 Image/Part，
    因此暫時寫到一個檔案再讀取。
    """
    # 先寫到暫存檔
    temp_filename = f"temp_{uuid.uuid4()}.png"
    with open(temp_filename, "wb") as f:
        f.write(image_data)

    try:
        # 讀取本地檔
        vertex_img = VertexImage.load_from_file(temp_filename)
        # 組合 prompt
        prompt = (
            "使用繁體中文來進行以下操作: Turn this image into a meme. "
            "Give me a short, funny sentence (3-5 words). No Markdown. "
            "No explaination texts, only the best choice needed. "
            "Avoid any offensive or inappropriate content."
        )
        # 以多模態方式呼叫
        response = model.generate_content([
            Part.from_image(vertex_img),
            prompt
        ])
        text = response.text.strip()
    finally:
        # 呼叫結束後，刪除暫存檔
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    return text

def create_meme_image(input_image: Image.Image, text: str) -> Image.Image:
    """
    將原圖嵌入黑色邊框，並在下方加上 `me when I: text` 這樣的梗圖文字。
    """

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
    font_size = int(w * 0.07)  # 字體大小為圖片寬度的5%，可以依需求調整
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

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    """
    從 Caller 收到圖片 bytes -> 以記憶體方式呼叫 Gemini 分析 -> 
    將類型結果加到浮水印 -> 回傳處理後圖片
    """
    # 讀取圖片 bytes
    image_data = await file.read()
    
    # 用 Pillow 開啟圖片
    try:
        pil_image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        return {"error": f"無法讀取上傳圖片: {e}"}

    output_image = create_meme_image(pil_image, generate_meme_text(image_data))
    
   # 不再依賴檔名，而是直接使用 PIL 自動偵測原圖格式
    fmt = pil_image.format if pil_image.format else "JPEG"

    # 如果輸出為 JPEG，則轉回 RGB（JPEG不支援alpha）
    if fmt.upper() == "JPEG":
        output_image = output_image.convert("RGB")
    
    buf = io.BytesIO()
    output_image.save(buf, format=fmt)  
    buf.seek(0)
    
    # 以二進位串流形式回傳
    media_type = "image/png" if fmt == "PNG" else "image/jpeg"
    return Response(content=buf.getvalue(), media_type=media_type)