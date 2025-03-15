import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
from dotenv import load_dotenv
import os

load_dotenv()

# 初始化 Vertex AI 環境
vertexai.init(project=os.getenv('PROJECTID'), location=os.getenv('REGION'))  # 確保地區與模型相符

# 載入 Gemini Vision 模型（例如最新版本名稱，可在 Vertex AI 模型頁面查詢）
model = GenerativeModel(model_name="gemini-2.0-flash-001")

# 準備要分析的圖片及提示詞
vertex_image = Image.load_from_file("./example.jpg")  # 從本地檔案載入圖片
prompt = "這張照片主要是風景、人像還是物體？只回答類別名稱。"

# 呼叫模型進行內容生成（分析）
response = model.generate_content([Part.from_image(vertex_image), prompt])
result_text = response.text.strip()
print("分析結果:", result_text)
