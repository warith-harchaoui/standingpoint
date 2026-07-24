"""FastAPI backend for the Standpoint browser GUI (investigation, `dev-gui` branch).

This is the thin server behind the single-page GUI: it turns an edited table into a
positioning result the browser can render. The heavy lifting stays in the library —
`positioning()` runs the PCA, orientation, colouring, LLM pole naming, and analysis;
this module only exposes it over HTTP and serves the static page.

Endpoints
---------
GET  /             redirect to the GUI.
GET  /gui          the single-page editor + viewer (see `webgui.GUI_HTML`).
GET  /api/example  a starter table (CSV text) to populate the grid.
POST /api/position from an edited table, return the Vega-Lite spec + Markdown + YAML.

Run it with ``standpoint-gui`` (installed by the ``gui`` extra) or
``uvicorn standpoint.api:app``. It is intentionally *not* imported by the core
package, so the library and CLIs carry no web dependency.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel

from standpoint import DEFAULT_MODEL, analysis_markdown, positioning
from standpoint.webgui import GUI_HTML

app = FastAPI(title="Standpoint GUI", version="0.1.0")

# A small starter table shipped so the grid is never empty on first load.
_STARTER_TABLE = (
    "Language,Performance,Ease of Learning,Ecosystem,Concurrency,Type Safety,Job Market,Tooling\n"
    "Python,2,5,5,2,2,5,4\n"
    "Rust,5,2,3,5,5,3,4\n"
    "Go,4,4,4,5,4,4,4\n"
    "JavaScript,3,4,5,3,2,5,3\n"
    "Java,4,3,5,4,4,5,4\n"
)


class PositionRequest(BaseModel):
    """Body of ``POST /api/position`` — one edited table plus a few options.

    Attributes
    ----------
    table : str
        The edited comparison table as CSV text (first column = option names).
    reference : str
        Row index (as a string) or exact option name to place top-right.
    lower : str
        Comma-separated criteria where lower is better (e.g. ``"Price,Weight"``).
    use_llm : bool
        Whether to name the axes and write the analysis with the local model.
    model : str
        Ollama model to use when ``use_llm`` is true.
    """

    table: str
    reference: str = "0"
    lower: str = ""
    use_llm: bool = False
    model: str = DEFAULT_MODEL


class PositionResponse(BaseModel):
    """What the browser needs to draw the quadrant and show the write-up."""

    vega: dict
    markdown: str
    yaml: str
    axes: dict[str, str]
    poles: list[str]
    reference: str
    roles: dict[str, str]


@app.get("/", include_in_schema=False)
def index() -> RedirectResponse:
    """Redirect the site root to the GUI page."""
    return RedirectResponse(url="/gui")


@app.get("/gui", response_class=HTMLResponse, include_in_schema=False)
def gui() -> str:
    """Serve the single-page table editor + quadrant viewer."""
    return GUI_HTML


@app.get("/api/example", response_class=PlainTextResponse)
def example() -> str:
    """Return a starter table (CSV text) to populate an empty grid."""
    return _STARTER_TABLE


@app.post("/api/position", response_model=PositionResponse)
def position(req: PositionRequest) -> PositionResponse:
    """Run the full positioning on an edited table and return everything to draw it.

    Parameters
    ----------
    req : PositionRequest
        The edited table and options from the browser.

    Returns
    -------
    PositionResponse
        The Vega-Lite spec (rendered client-side by vega-embed), the Markdown
        interpretation, the YAML dump, and the axis names / poles / roles.

    Raises
    ------
    HTTPException
        400 if the table is empty or degenerate, or the reference is unknown —
        the library's ``ValueError`` message is passed straight through to the UI.
    """
    if not req.table.strip():
        raise HTTPException(status_code=400, detail="The table is empty.")
    # A numeric reference arrives as a string ("0"); pass ints through as ints so
    # `positioning` treats it as a row index rather than an option name.
    ref: int | str = int(req.reference) if req.reference.lstrip("-").isdigit() else req.reference
    lower = [c.strip() for c in req.lower.split(",") if c.strip()]
    try:
        pos = positioning(
            req.table,
            reference=ref,
            lower_is_better=lower,
            model=req.model,
            use_llm=req.use_llm,
        )
    except ValueError as exc:  # bad table / unknown reference -> a clean 400 for the UI
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # The Markdown narrative is a separate call so a slow model doesn't block the
    # spec; here we compute it inline since the whole request is already synchronous.
    markdown = analysis_markdown(
        pos.result, pos.roles, pos.poles, model=req.model, use_llm=req.use_llm
    )
    return PositionResponse(
        vega=pos.to_vega(),
        markdown=markdown,
        yaml=pos.to_yaml(),
        axes=pos.axes,
        poles=pos.poles,
        reference=pos.result.reference,
        roles=pos.role_of,
    )


def main_gui() -> None:
    """Console entry point (``standpoint-gui``): serve the GUI on localhost:8000."""
    import uvicorn

    # Local-first: bind to loopback only, so the table never leaves the machine.
    print("Standpoint GUI -> http://localhost:8000/gui  (Ctrl-C to stop)")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main_gui()
