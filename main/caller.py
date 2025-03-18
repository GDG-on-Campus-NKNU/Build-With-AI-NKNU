import os
import requests
from tqdm import tqdm
from tkinter import Tk, filedialog
import io
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor


def select_file():
    """呼叫檔案對話框讓使用者選取圖片檔案"""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="請選擇圖片檔案", 
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    return file_path

def upload_in_memory(api_url: str, file_path: str):
    """
    讀取圖片為 bytes, 透過 requests.post(files=...) 直接傳給後端
    並用 tqdm 顯示上傳與下載進度
    """
    if not file_path or not os.path.exists(file_path):
        print("檔案不存在，請重新選擇。")
        return
    
    # 讀取檔案到記憶體
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    
    # 進度條 (上傳)
    print("上傳圖片中...")
    with tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading') as pbar:
        def progress_cb(monitor):
            # monitor.bytes_read: requests 已讀取的位元組
            pbar.update(monitor.bytes_read - pbar.n)

        # 使用 requests_toolbelt 來實作 progress callback
        encoder = MultipartEncoder(fields={'file': (os.path.basename(file_path), io.BytesIO(file_bytes), 'application/octet-stream')})
        monitor = MultipartEncoderMonitor(encoder, progress_cb)
        
        response = requests.post(api_url, data=monitor, headers={'Content-Type': monitor.content_type}, stream=True)
        pass
    
    if response.status_code != 200:
        print("處理失敗:", response.text)
        return
    
    # 從 Content-Type 獲取圖片格式
    content_type = response.headers.get("Content-Type", "image/jpeg")
    if content_type == "image/png":
        file_ext = ".png"
        file_type = [("PNG files", "*.png"), ("All files", "*.*")]
    else:
        file_ext = ".jpg"
        file_type = [("JPEG files", "*.jpg"), ("All files", "*.*")]
    
    # 進度條 (下載)
    total_size = int(response.headers.get("Content-Length", 0))
    print("處理完成，下載結果中...")
    
    # 呼叫檔案對話框讓使用者選擇儲存位置
    root = Tk()
    root.withdraw()
    output_name = filedialog.asksaveasfilename(
        title="儲存處理後的圖片",
        defaultextension=file_ext,
        filetypes=file_type
    )
    
    if not output_name:
        print("未選擇儲存位置，下載取消。")
        return
    
    with open(output_name, "wb") as f, tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading') as pbar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    print(f"處理後圖片已存檔: {output_name}")

def main():
    api_url = "http://localhost:8000/process-image"
    print("=== 圖片處理 Caller ===")
    print("輸入 'upload' 選取圖片，輸入 'exit' 離開")

    while True:
        cmd = input("> ").strip().lower()
        if cmd == "upload":
            path = select_file()
            if path:
                upload_in_memory(api_url, path)
        elif cmd == "exit":
            print("離開程式")
            break
        else:
            print("未知指令，請輸入 'upload' 或 'exit'。")

if __name__ == "__main__":
    main()
