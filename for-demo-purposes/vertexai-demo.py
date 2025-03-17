import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
from dotenv import load_dotenv
import os

load_dotenv()

vertexai.init(project=os.getenv('PROJECTID'), location=os.getenv('REGION'))

model = GenerativeModel(model_name="gemini-2.0-flash-001")

vertex_image = Image.load_from_file("for-demo-purposes/example.jpg")
prompt = "這張照片主要是風景、人像還是物體？只回答類別名稱。"

response = model.generate_content([Part.from_image(vertex_image), prompt])
result_text = response.text.strip()
print("分析結果:", result_text)
