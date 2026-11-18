from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated




from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates



from api.api_transform import run_actions
from api.schemas import Token, UserCreate, UserPublic
from api.security import authenticate_user, create_access_token, get_current_user, hash_password
from database.database import create_databases , create_user, get_history

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_databases()
    yield





app = FastAPI(lifespan=lifespan)




BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = get_current_user()
    
    # if user :
    #     return templates.TemplateResponse(request, "index.html", {"name": user.username,"history": get_history()})
    # else:
    return templates.TemplateResponse(request, "login.html")

@app.get("/analyze", response_class=HTMLResponse)
async def analysis(
    request: Request):
    user = get_current_user()
    return templates.TemplateResponse(request, "index.html")
    

@app.post("/analyze/text", response_class=HTMLResponse)
async def text_result(
    request: Request,
    text: str = Form(...),
    transform: str = Form(""),
    statistic: str = Form(""),
    frequent: int = Form(5, ge=1, le=10),
):
    ctx = {"name": "world", "active_tab": "text", "history": get_history()}
    if not transform and not statistic:
        ctx["error"] = {"message": "Select at least one action"}
    else:
        ctx.update(run_actions(text, transform, statistic, frequent))
        ctx["history"] = get_history()
 
    return templates.TemplateResponse(request, "index.html", ctx)

@app.post("/analyze/file", response_class=HTMLResponse)
async def analyze_file(request: Request, file: UploadFile = File(...),transform: str = Form(""),
    statistic: str = Form(""), frequent: int = Form(5, ge=1, le=10)):
    ctx = {"name": "world", "active_tab": "file","file_name": file.filename, "history": get_history()}

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
        ctx["history"] = get_history()

    return templates.TemplateResponse(request, "index.html", ctx)


@app.post("/register", status_code=201, summary="Create a new user")
def register_user(
    username: str = Form(..., min_length=3, max_length=20),
    password: str = Form(..., min_length=6),
    full_name: str = Form(...),
    ):
    hashed = hash_password(password)
    if not create_user(username, hashed, full_name):
        raise HTTPException(status_code=409, detail="Username already taken")
    return RedirectResponse(url="/", status_code=303)


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
   
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user["username"]})
    response= RedirectResponse(url="/analyze",status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=3600
    )
    return response

@app.get("/me", response_model=UserPublic, summary="Get my profile (protected)")
def read_me(current_user: UserPublic = Depends(get_current_user)):
    return current_user

@app.on_event("startup")
def on_startup():
    create_databases()