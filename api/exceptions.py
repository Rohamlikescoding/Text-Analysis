from urllib.parse import quote

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException


class NotAuthenticated(Exception):
    def __init__(self, message: str = "Please log in to continue."):
        self.message = message


async def not_authenticated_handler(request: Request, exc: NotAuthenticated):
    wants_html = "text/html" in request.headers.get("accept", "")
    if not wants_html:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = RedirectResponse(
        url=f"/login?error={quote(exc.message)}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.delete_cookie("access_token")
    return response


async def http_exception_redirect_handler(
    request: Request, exc: StarletteHTTPException
):
    wants_html = "text/html" in request.headers.get("accept", "")

    if exc.status_code == 405 and wants_html:
        if request.cookies.get("access_token"):
            return RedirectResponse(
                url=f"/analyze?error={quote("That page can't be opened directly")}",
                status_code=status.HTTP_303_SEE_OTHER,
            )

        return RedirectResponse(
            url=f"/login?error={quote('Please log in to continue.')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    # everything else (404, your own HTTPExceptions, API clients) behaves as before
    return await http_exception_handler(request, exc)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotAuthenticated, not_authenticated_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_redirect_handler)
