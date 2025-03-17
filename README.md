# Build With AI NKNU: AI Meme Generator with Vertex AI & Gemini Vision

這是一個使用 Google Vertex AI 與 Gemini Vision 模型打造的小型 AI 應用示範專案，目的在於展示如何透過生成式 AI 為圖片產生有趣的敘述，進一步快速製作梗圖。

## 🎯 專案特色

- **多模態 AI 整合**：使用 Gemini Vision 模型分析圖片並生成幽默短句。
- **即時圖片處理**：透過 Pillow 套件將文字與圖片合成，產生趣味的梗圖。
- **簡潔 API 介面**：使用 FastAPI 架設後端服務，提供簡單易懂的 API 範例。
- **直觀操作體驗**：提供終端機呼叫端（caller），使用者能直覺上傳與下載處理後圖片。

## 🚀 如何開始

### 1. 安裝需求

首先，確保你已經安裝 Python (version 3.8+)，並且下載此專案：

```bash
git clone https://github.com/GDG-on-Campus-NKNU/Build-With-AI-NKNU
cd Build-With-AI-NKNU
```

設置虛擬環境：
```bash
py -m venv env
env/Scripts/activate
```

安裝相關套件：

```bash
pip install -r requirements.txt
```

### 2. 設定 Google Cloud 環境

此專案使用 Google Vertex AI 服務，因此你需要：

- 擁有一個 Google Cloud 專案並啟用 Vertex AI API。
- 取得專案 ID 與模型所在區域（例如 `us-central1`）。
- 進行 Google Cloud 認證：

```bash
gcloud auth application-default login
```

或將你的服務帳戶 JSON 憑證下載到本機，並設定環境變數：

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service_account.json"
```

### 3. 修改環境變數

請在專案根目錄建立 `.env` 檔案，內容如下：

```env
PROJECTID="your-gcp-project-id"
REGION="us-central1"
```

### 4. 啟動伺服器

在本機啟動 FastAPI 後端伺服器：

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 使用 Caller 呼叫 API

啟動互動式終端 Caller：

```bash
python meme_caller.py
```

- 輸入 `upload` 後，即可選擇圖片上傳。
- 下載處理完成的梗圖，享受 AI 帶來的趣味體驗。

## 🔨 專案結構

```
.
├── for-demo-purposes        # 示範用途的範例程式
│   ├── example.jpg
│   ├── fastapi_demo.py
│   ├── meme.jpg
│   ├── memify_demo.py
│   └── vertexai_demo.py
├── main                     # 主要應用程式程式碼
│   ├── caller.py            # 終端機呼叫端
│   └── server.py            # FastAPI 後端伺服器
├── .env                     # 存放環境變數
├── .gitignore               # Git 忽略檔案設定
├── entry.py                 # 伺服器啟動程式
├── README.md                # 專案說明文件
└── requirements.txt         # 套件需求清單
```

## 📌 課程示範用途說明

本專案主要用於示範 Google Vertex AI 與 Gemini Vision 模型的基本用法，課堂中會：

- 講解生成式 AI 的基礎概念。
- 示範如何透過 Python 呼叫 Google Vertex AI API。
- 展示一個實際的 AI 應用流程：從圖片分析到梗圖生成。

由於課程時間限制，將聚焦於技術介紹與實際 API 呼叫示範，並不會完整實作所有功能細節。

## 📚 延伸學習

若你希望進一步了解更多 Google Cloud 服務與生成式 AI 技術，可參考官方資源：

- [Vertex AI 官方文件](https://cloud.google.com/vertex-ai/docs)
- [Google Generative AI Studio](https://cloud.google.com/generative-ai/docs)

## 貢獻者

[Bernie (Unforgettableeternalproject)](https://github.com/Unforgettableeternalproject)

電子郵件: [![Static Badge](https://img.shields.io/badge/mail-Bernie-blue)
](mailto:ptyc4076@gmail.com)

---

✨ 祝你享受 AI 帶來的樂趣，讓我們一起 Build with AI！

