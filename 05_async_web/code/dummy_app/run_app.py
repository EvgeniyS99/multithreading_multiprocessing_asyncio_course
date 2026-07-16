import uvicorn
from dummy_app import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9999)

# curl -X POST http://127.0.0.1:9999/inference \
#   -H "Content-Type: application/json" \
#   -d '{"text":"hello"}'