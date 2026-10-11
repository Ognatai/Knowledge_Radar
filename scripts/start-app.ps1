<#
.SYNOPSIS
    Start the local app: chat UI, API and both indices in Docker.
.DESCRIPTION
    Starts the private index (scripts/start-neo4j.ps1 -Private), then the public
    index, the API and the chat UI (docker-compose.yml), with the private checkout
    from local-config.yaml mounted into the API (docker-compose.app-private.yml). Both Neo4j passwords come
    from the Windows Credential Manager and are passed to Docker Compose for this
    process only; they are never written to a file. Ollama stays a host
    installation and must be running. Opens http://127.0.0.1:8080 when ready.

    -NoPrivate starts without the private index; the chat then answers from the
    public knowledge base only and says so.
#>
[CmdletBinding()]
param(
    [switch]$NoPrivate,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$repository = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repository ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

function Get-Secret([string]$user) {
    $secret = & $python -m keyring get knowledge-radar $user
    if (-not $secret) {
        throw "No password for '$user' in the Credential Manager. Run: python -m keyring set knowledge-radar $user"
    }
    return $secret
}

function Test-Url([string]$url) {
    try {
        Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5 | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is not installed or not on PATH (see SETUP.md)."
}
if (-not (Test-Url "http://127.0.0.1:11434/api/version")) {
    Write-Warning "Ollama does not answer on port 11434; start it, or the chat cannot answer."
}

if (-not $NoPrivate) {
    & (Join-Path $PSScriptRoot "start-neo4j.ps1") -Private
}

$composeFiles = @("-f", (Join-Path $repository "docker-compose.yml"))
$env:NEO4J_PASSWORD = Get-Secret "neo4j"
if (-not $NoPrivate) {
    $env:NEO4J_PRIVATE_PASSWORD = Get-Secret "neo4j-private"
    # The private checkout from local-config.yaml, mounted for the interview commands.
    Push-Location $repository
    try {
        $privateRepo = & $python -c "from app.backend.knowledge_radar.config import load_local_config; p = load_local_config().private_repo_path; print(p or '')"
    } finally {
        Pop-Location
    }
    if ($LASTEXITCODE -ne 0) {
        throw "local-config.yaml could not be read (see the error above)."
    }
    if ($privateRepo) {
        $env:KNOWLEDGE_RADAR_PRIVATE_REPO_HOST = $privateRepo
        $composeFiles += @("-f", (Join-Path $repository "docker-compose.app-private.yml"))
    } else {
        Write-Warning "No private_repo_path in local-config.yaml: the chat runs, the interview commands are off."
    }
}
try {
    # Docker reports progress on stderr; Windows PowerShell would treat that as an error.
    $ErrorActionPreference = "Continue"
    docker compose --project-directory $repository @composeFiles up -d --build web api neo4j
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose failed with exit code $LASTEXITCODE"
    }
}
finally {
    $ErrorActionPreference = "Stop"
    Remove-Item Env:NEO4J_PASSWORD -ErrorAction SilentlyContinue
    Remove-Item Env:NEO4J_PRIVATE_PASSWORD -ErrorAction SilentlyContinue
    Remove-Item Env:KNOWLEDGE_RADAR_PRIVATE_REPO_HOST -ErrorAction SilentlyContinue
}

$deadline = (Get-Date).AddSeconds(90)
while (-not (Test-Url "http://127.0.0.1:8080/api/health")) {
    if ((Get-Date) -gt $deadline) {
        throw "The app did not answer on http://127.0.0.1:8080 within 90 seconds; see: docker logs knowledge_radar-api-1"
    }
    Start-Sleep -Seconds 3
}
Write-Host "Knowledge Radar: http://127.0.0.1:8080"
if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:8080"
}
