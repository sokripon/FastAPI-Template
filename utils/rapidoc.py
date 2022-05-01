from starlette.requests import Request
from starlette.responses import HTMLResponse


def get_html(request: Request) -> HTMLResponse:
    return HTMLResponse(f"""
            <!doctype html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <script 
                        type="module" 
                        src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"
                    ></script>
                </head>
                <body>
                    <rapi-doc spec-url="{request.app.openapi_url}"></rapi-doc>
                </body> 
            </html>
            """)
