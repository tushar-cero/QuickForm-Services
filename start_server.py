import uvicorn

APP_MODULE = "main:app"
HOST = "127.0.0.1"
PORT = 8000
RELOAD = True
LOG_LEVEL = "info"
WORKERS = 1

if __name__ == "__main__":
    print(f"Starting Uvicorn server for '{APP_MODULE}'...")
    print(f"Listening on: http://{HOST}:{PORT}")

    uvicorn.run(
        APP_MODULE,
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level=LOG_LEVEL,
        workers=WORKERS
    )

    # You can add more sophisticated argument parsing (using argparse)
    # or configuration loading (from .env files, etc.) here if needed.