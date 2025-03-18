import subprocess
import time

# Start FastAPI backend
print("Starting FastAPI backend...")
backend_process = subprocess.Popen(["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"])

# Give the backend some time to start
time.sleep(3)

# Start Streamlit frontend
print("Starting Streamlit frontend...")
frontend_process = subprocess.Popen(["streamlit", "run", "chat_ui.py"])

# Keep the script running
backend_process.wait()
frontend_process.wait()