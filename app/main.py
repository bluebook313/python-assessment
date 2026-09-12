from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import router as api_router
from schemas.config import ServerIp, ServerPort, ReloadServer
import uvicorn

app = FastAPI(docs_url=None)
app.include_router(api_router)
app.mount(
    "/static",
    StaticFiles(directory="./static"),
    name="static",
    )


from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="API Docs",
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",          # module:app_instance
        host=ServerIp,
        port=ServerPort,
        reload=ReloadServer,         # auto-reload on code changes
    )