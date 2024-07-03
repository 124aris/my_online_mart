from fastapi import FastAPI

app = FastAPI(title = "User Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8005",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "User Service"}