import os
import ctypes

# Ép thêm đường dẫn CUDA vào hệ thống load DLL của Python
cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2\bin"
os.add_dll_directory(cuda_path)

try:
    from llama_cpp import Llama
    print("THÀNH CÔNG: Đã load được thư viện!")
    llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", n_gpu_layers=-1)
    print("Mô hình đã nằm trên GPU!")
except Exception as e:
    print(f"LỖI THỰC TẾ: {e}")