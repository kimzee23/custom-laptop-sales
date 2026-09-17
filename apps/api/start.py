import os
import sys

if __name__ == "__main__":
    port_str = os.environ.get("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        port = 8000

    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting Custom Laptop API on {host}:{port}...", flush=True)

    import uvicorn
    uvicorn.run("app.main:app", host=host, port=port, log_level="info")
