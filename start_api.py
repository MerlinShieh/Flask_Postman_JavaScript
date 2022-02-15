import os

cmd = "powershell Start-Process -WindowStyle hidden -FilePath python  api_base64_to_img.py"
os.system(cmd)