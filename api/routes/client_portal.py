from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from api.routes.client_portal_page import render_client_portal_html

router = APIRouter()


@router.get("/portal", response_class=HTMLResponse)
async def client_portal_shell() -> str:
    return render_client_portal_html()
