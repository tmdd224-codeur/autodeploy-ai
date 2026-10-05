from fastapi import FastAPI

app = FastAPI(
    title="AutoDeploy AI API",
    description="API pour notre plateforme DevSecOps intelligente",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AutoDeploy AI fonctionne !",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
