import re
from fastapi import FastAPI, Header, HTTPException, Request
from typing import Annotated


app = FastAPI()


def check_accept_language(request: Request):
    pattern = re.compile(
        r"^[a-zA-Z]{2}(?:-[a-zA-Z]{2})?(?:,[a-zA-Z]{2}(?:-[a-zA-Z]{2})?(?:;\s?q=\d\.\d)?)*$")
    if not re.match(pattern, request.headers["Accept-Language"]):
        raise HTTPException(
            status_code=400,
            detail="Incorrect header The Accept-Language format")


@app.get("/headers")
def get_headers(request: Request):
    if "User-Agent" not in request.headers:
        raise HTTPException(
            status_code=400, detail="The User-Agent not found!")
    if "Accept-Language" not in request.headers:
        raise HTTPException(
            status_code=400, detail="The Accept-Language not found!")
    check_accept_language(request)
    return {"User-Agent": request.headers["User-Agent"],
            "Accept-Language": request.headers["Accept-Language"]}


# альтернативный вариант:


# def check_accept_language(request: Request):
#     pattern = r"(?i:(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?,)+(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?"
#     if not re.fullmatch(pattern, request.headers["Accept-Language"]):
#         raise HTTPException(
#             status_code=400,
#             detail="Incorrect header The Accept-Language format"
#         )

# @app.get("/headers")
# def get_headers(user_agent: Annotated[str | None, Header()] = None,
#                 accept_language: Annotated[str | None, Header()] = None):
#     if user_agent is None or accept_language is None:
#         raise HTTPException(
#             status_code=400,
#             detail="The User-Agent or Accept-Language not found!")
#     return {"User-Agent": user_agent,
#             "Accept-Language": accept_language}
