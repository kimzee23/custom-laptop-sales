import sys
import os
import traceback

log_file = open("server_debug.log", "w", encoding="utf-8", buffering=1)
sys.stdout = log_file
sys.stderr = log_file

print(f"Python: {sys.executable}", flush=True)
print(f"Version: {sys.version}", flush=True)

try:
    import fastapi
    print("FastAPI imported successfully", flush=True)
except Exception as e:
    print(f"FastAPI import error: {e}", flush=True)

try:
    import uvicorn
    print("Uvicorn imported successfully", flush=True)
except Exception as e:
    print(f"Uvicorn import error: {e}", flush=True)

try:
    from app.main import app
    print("app.main:app imported successfully", flush=True)
except Exception as e:
    print("Error importing app:", flush=True)
    traceback.print_exc(file=log_file)

if __name__ == "__main__":
    try:
        import uvicorn
        print("Starting uvicorn.run... application starting", flush=True)
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print("Error in uvicorn.run:", flush=True)
        traceback.print_exc(file=log_file)
