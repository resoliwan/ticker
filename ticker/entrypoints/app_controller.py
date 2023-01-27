from fastapi import FastAPI

# logger = logging.getLogger(__name__)
# bus, dep = bootstrap.bootstrap()

app = FastAPI()


@app.get("/tk/version/v1")
def get_version():
    return {"success": True, "version": "0.0.0"}


@app.get("/tk/ticker/v1")
def get_ticker(symbol, interval, range):
    return True


@app.post("/tk/ticker/v1")
def save_ticker(symbol, interval, range):
    return True
