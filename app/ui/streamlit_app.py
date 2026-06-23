# ui/streamlit_app.py - thin UI layer; delegates to app.services

import json
import os

import requests
import streamlit as st

DEFAULT_API_URL = os.getenv("DIALAGENT_API_URL", "http://localhost:8000")


def _api_url() -> str:
    return st.session_state.get("api_url", DEFAULT_API_URL).rstrip("/")


@st.cache_data(ttl=10, show_spinner=False)
def _check_api_health(api_url: str) -> tuple[bool, int | None]:
    try:
        health = requests.get(f"{api_url}/health", timeout=3)
        return health.ok, health.status_code
    except requests.RequestException:
        return False, None


def _load_index_stats() -> dict:
    try:
        resp = requests.get(f"{_api_url()}/index/stats", timeout=10)
        if resp.ok:
            return resp.json()
    except requests.RequestException:
        pass
    return {"total_chunks": 0, "sources": [], "db_path": "unknown"}


def _render_indexed_files(stats: dict) -> None:
    st.subheader("Indexed knowledge base")
    st.caption(f"Vector store: `{stats.get('db_path', 'unknown')}`")

    sources = stats.get("sources", [])
    if not sources:
        st.info("No files indexed yet. Use the **Index** tab or run `python cli.py ingest`.")
        return

    st.metric("Total chunks", stats.get("total_chunks", 0))
    st.dataframe(
        [{"File": s["filename"], "Chunks": s["chunks"]} for s in sources],
        width="stretch",
        hide_index=True,
    )


def page_convert():
    st.header("Document -> Markdown")
    st.caption("Upload a PDF, Word doc, or menu image. OCR runs automatically on images.")

    uploaded = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "md"],
    )
    force_ocr = st.checkbox("Force OCR", value=False, help="Useful for scanned PDFs")

    if st.button("Convert", type="primary", disabled=uploaded is None):
        with st.spinner("Converting..."):
            files = {"file": (uploaded.name, uploaded.getvalue())}
            data = {"force_ocr": str(force_ocr).lower()} if force_ocr else {}
            resp = requests.post(f"{_api_url()}/convert", files=files, data=data, timeout=600)
            resp.raise_for_status()
            result = resp.json()

        st.success(
            f"Converted **{result['filename']}** "
            f"({result['char_count']:,} chars, OCR: {'yes' if result['ocr_used'] else 'no'})"
        )
        st.download_button(
            "Download markdown",
            data=result["markdown"],
            file_name=f"{os.path.splitext(result['filename'])[0]}.md",
            mime="text/markdown",
        )
        st.markdown("### Preview")
        st.markdown(result["markdown"])


def _api_post(path: str, **kwargs):
    resp = requests.post(f"{_api_url()}{path}", **kwargs)
    if not resp.ok:
        detail = resp.text
        try:
            detail = resp.json().get("detail", detail)
        except ValueError:
            pass
        st.error(f"API error ({resp.status_code}): {detail}")
        st.stop()
    return resp.json()


def page_query():
    st.header("RAG Query")
    question = st.text_area("Question", placeholder="Quels plats vegetariens proposez-vous ?")

    if st.button("Ask", type="primary", disabled=not question.strip()):
        with st.spinner("Searching and generating..."):
            response = _api_post("/query", json={"query": question}, timeout=300)

        st.markdown("### Answer")
        st.write(response.get("answer", ""))
        if response.get("action"):
            st.info(f"Action: `{response['action']}`")
        with st.expander("Raw JSON"):
            st.code(json.dumps(response, indent=2, ensure_ascii=False), language="json")


def page_index():
    st.header("Index a document")
    st.caption("Convert and add a file to the vector store for RAG queries.")

    uploaded = st.file_uploader(
        "File to index",
        type=["pdf", "docx", "png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "md"],
        key="index_upload",
    )
    force_ocr = st.checkbox("Force OCR", value=False, key="index_ocr")

    if st.button("Index", type="primary", disabled=uploaded is None):
        with st.spinner("Converting and indexing..."):
            files = {"file": (uploaded.name, uploaded.getvalue())}
            data = {"force_ocr": str(force_ocr).lower()} if force_ocr else {}
            result = _api_post(
                "/convert-and-index",
                files=files,
                data=data,
                timeout=600,
            )

        st.success("File indexed successfully")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("File", result["filename"])
        col2.metric("Format", result.get("format", "-"))
        col3.metric("Characters", f"{result['char_count']:,}")
        col4.metric("Chunks", result["chunks_indexed"])
        st.caption(f"OCR used: {'yes' if result.get('ocr_used') else 'no'}")

    st.divider()
    _render_indexed_files(_load_index_stats())


def main():
    st.set_page_config(page_title="DialAgent Demo", page_icon="🍽️", layout="wide")
    st.title("DialAgent Demo")
    st.sidebar.text_input("API URL", value=DEFAULT_API_URL, key="api_url")

    ok, status_code = _check_api_health(_api_url())
    if ok:
        st.sidebar.success("API connected")
    elif status_code is not None:
        st.sidebar.warning(f"API returned {status_code}")
    else:
        st.sidebar.error("API unreachable - start with scripts/run_api.ps1")

    tab_convert, tab_query, tab_index = st.tabs(["Convert", "RAG Query", "Index"])

    with tab_convert:
        page_convert()
    with tab_query:
        page_query()
    with tab_index:
        page_index()


if __name__ == "__main__":
    main()
