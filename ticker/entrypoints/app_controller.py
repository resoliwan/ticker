from fastapi import FastAPI

# logger = logging.getLogger(__name__)
# bus, dep = bootstrap.bootstrap()

app = FastAPI()


@app.get("/ticker/version/v1")
def get_version():
    # version
    return {"success": True, "version": "0.0.0"}
