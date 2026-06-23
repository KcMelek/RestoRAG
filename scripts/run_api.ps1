# Start the document conversion + RAG API
Set-Location $PSScriptRoot\..
$reload = $env:DIALAGENT_API_RELOAD
if ($reload -and $reload -ne "0" -and $reload.ToLower() -ne "false") {
    python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
} else {
    python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
}
