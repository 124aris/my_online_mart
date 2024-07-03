from fastapi import FastAPI

app = FastAPI(title = "Payment Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8003",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "Payment Service"}