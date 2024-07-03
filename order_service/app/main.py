from fastapi import FastAPI

app = FastAPI(title = "Order Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8002",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "Order Service"}