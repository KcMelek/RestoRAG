# Start the Streamlit demo UI (expects API at http://localhost:8000 unless changed in sidebar)
Set-Location $PSScriptRoot\..
$env:DIALAGENT_API_URL = if ($env:DIALAGENT_API_URL) { $env:DIALAGENT_API_URL } else { "http://localhost:8000" }
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$PSScriptRoot\..;$env:PYTHONPATH" } else { "$PSScriptRoot\.." }
streamlit run app/ui/streamlit_app.py
