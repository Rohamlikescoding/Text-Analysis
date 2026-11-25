from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote


from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates


from api.api_transform import run_actions
from api.exceptions import register_exception_handlers
from api.schemas import UserPublic
from api.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    hash_password,
    strong_password,
)
from database.database import create_database, create_user, get_history


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def redirect_error(message: str):
    return RedirectResponse(url=f"/login?error={quote(message)}", status_code=303)


@app.get("/")
async def home(request: Request):
    if request.cookies.get("access_token"):
        return RedirectResponse(url="/analyze", status_code=303)
    return RedirectResponse(url="/login", status_code=303)


@app.get("/analyze", response_class=HTMLResponse)
async def analysis(
    request: Request,
    error: str | None = None,
    user: UserPublic = Depends(get_current_user),
):

    ctx = {
        "name": user.full_name,
        "active_tab": "text",
        "history": get_history(user.username),
    }
    if error:
        ctx["error"] = {"message": error}

    return templates.TemplateResponse(request, "index.html", ctx)


@app.post("/analyze/text", response_class=HTMLResponse)
async def text_result(
    request: Request,
    text: str = Form(...),
    transform: str = Form(""),
    statistic: str = Form(""),
    frequent: int = Form(5, ge=1, le=10),
    user: UserPublic = Depends(get_current_user),
):
    ctx = {
        "name": user.full_name,
        "active_tab": "text",
        "history": get_history(user.username),
    }
    if not transform and not statistic:
        ctx["error"] = {"message": "Select at least one action"}
    else:
        ctx.update(run_actions(text, transform, statistic, frequent, user.username))
        ctx["history"] = get_history(user.username)

    return templates.TemplateResponse(request, "index.html", ctx)


@app.post("/analyze/file", response_class=HTMLResponse)
async def analyze_file(
    request: Request,
    file: UploadFile = File(...),
    transform: str = Form(""),
    statistic: str = Form(""),
    frequent: int = Form(5, ge=1, le=10),
    user: UserPublic = Depends(get_current_user),
):
    ctx = {
        "name": user.full_name,
        "active_tab": "file",
        "file_name": file.filename,
        "history": get_history(user.username),
    }

    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        ctx["error"] = {"message": str(e)}
        return templates.TemplateResponse(request, "index.html", ctx)

    if not transform and not statistic:
        ctx["error"] = {"message": "Select at least one action"}
    else:
        ctx.update(run_actions(text, transform, statistic, frequent, user.username))
        ctx["history"] = get_history(user.username)

    return templates.TemplateResponse(request, "index.html", ctx)


@app.post("/register", status_code=201, summary="Create a new user")
def register_user(
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
):

    username = username.strip()
    if not 3 <= len(username) <= 20:
        return redirect_error("Username must be between 3 and 20 characters")

    if not strong_password(password):
        return redirect_error(
            "Enter strong password, needs to contain at least 6 digits length, uppercase, lowercase, digits and special symbols"
        )

    hashed = hash_password(password)
    if not create_user(username, hashed, full_name):
        return redirect_error("Username already taken")

    return RedirectResponse(
        url=f"/login?success={quote("Acount Created successfully. Use your username and password to login")}",
        status_code=303,
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request, error: str | None = None, success: str | None = None
):
    return templates.TemplateResponse(
        request, "login.html", {"error": error, "success": success}
    )


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return RedirectResponse(
            url=f"/login?error={quote('Invalid username or password.')}",
            status_code=303,
        )
    access_token = create_access_token({"sub": user["username"]})
    response = RedirectResponse(url="/analyze", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=3600,
    )
    return response


@app.get("/logout", response_model=UserPublic, summary="Logout")
def read_me(current_user: UserPublic = Depends(get_current_user)):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
