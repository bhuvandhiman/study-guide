$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    throw 'The project environment is missing. Ask Codex to set it up or follow README.md.'
}
& $taskPython -m streamlit run app.py --server.headless true
