from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(
    title="AutoDeploy AI API",
    description="API pour notre plateforme DevSecOps intelligente",
    version="1.0.0"
)

REQUEST_COUNT = Counter(
    "autodeploy_http_requests_total",
    "Nombre total de requêtes HTTP"
)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.inc()
    return response


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


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
