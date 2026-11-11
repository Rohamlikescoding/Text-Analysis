from pathlib import Path

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api_transform import run_actions

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"name": "world"})


@app.post("/analyze/text", response_class=HTMLResponse)
async def text_result(
    request: Request,
    text: str = Form(...),
    transform: str = Form(""),
    statistic: str = Form(""),
    frequent: int = Form(""),
):
    ctx = {"name": "world", "active_tab": "text"}
    if not transform and not statistic:
        ctx["error"] = {"message": "Select at least one action"}
    else:
        ctx.update(run_actions(text, transform, statistic, frequent))
    return templates.TemplateResponse(request, "index.html", ctx)

@app.post("/analyze/file", response_class=HTMLResponse)
async def analyze_file(request: Request, file: UploadFile = File(...),transform: str = Form(""),
    statistic: str = Form(""), frequent: int = Form("")):
    ctx = {"name": "world", "active_tab": "file","file_name": file.filename}

    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        ctx["error"] = {"message": str(e)}
        return templates.TemplateResponse(request, "index.html", ctx)

    if not transform and not statistic:
        ctx["error"] = {"message": "Select at least one action"}
    else:
        ctx.update(run_actions(text, transform, statistic, frequent))
    return templates.TemplateResponse(request, "index.html", ctx)
