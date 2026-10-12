<#
.SYNOPSIS
    Set up a machine for the local app (chat, interview commands, Review Dashboard).
.DESCRIPTION
    Run from a fresh clone of this repository, e.g. on the ThinkPad. Each step is
    skipped when it is already done, so the script can be run again after fixing
    whatever stopped it:

      1. checks Git, Python 3.11+, Docker (running) and Ollama (answering)
      2. clones the private repository next to this one (-PrivateRepoUrl)
      3. creates .venv and installs the package, enables the git hooks
      4. writes local-config.yaml with the private checkout's path
      5. pulls the chat and embedding models
      6. asks for the secrets missing in the Credential Manager (neo4j,
         neo4j-private; the GitLab token is optional)
      7. starts both indices and builds them: public index, private structural
         graph, private extraction with the chat model, private index
      8. starts the app (scripts\start-app.ps1)

    Neo4j sets its password when its data volume is first created, so the two
    Neo4j passwords on this machine are new ones, independent of other machines.
.PARAMETER PrivateRepoUrl
    Clone URL of the private repository; needed only when it is not checked out yet.
.PARAMETER ChatModel
    The Ollama chat model, also used for the private extraction on this machine.
.PARAMETER SkipIndex
    Skip step 7, e.g. when the indices already exist.
#>
[CmdletBinding()]
param(
    [string]$PrivateRepoUrl,
    [string]$ChatModel = "qwen3:4b-instruct",
    [switch]$SkipIndex
)

$ErrorActionPreference = "Stop"
$repository = Split-Path -Parent $PSScriptRoot
$embeddingModel = "qwen3-embedding:0.6b"

function Step([string]$text) {
    Write-Host ""
    Write-Host "== $text" -ForegroundColor Cyan
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

function Invoke-Checked([string]$what, [scriptblock]$command) {
    # Native tools report progress on stderr; Windows PowerShell would treat that as an error.
    $ErrorActionPreference = "Continue"
    & $command
    $code = $LASTEXITCODE
    $ErrorActionPreference = "Stop"
    if ($code -ne 0) {
        throw "$what failed with exit code $code"
    }
}

Step "1. Prerequisites"
$missing = @()
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { $missing += "Git (winget install Git.Git)" }
$pythonVersion = if (Get-Command python -ErrorAction SilentlyContinue) { & python -c "import sys; print('%d.%d' % sys.version_info[:2])" } else { $null }
if (-not $pythonVersion -or [version]$pythonVersion -lt [version]"3.11") { $missing += "Python 3.11+ (winget install Python.Python.3.12)" }
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    $missing += "Docker Desktop (winget install Docker.DockerDesktop)"
} else {
    $ErrorActionPreference = "Continue"
    docker info --format "{{.ServerVersion}}" 2>&1 | Out-Null
    $dockerRunning = $LASTEXITCODE -eq 0
    $ErrorActionPreference = "Stop"
    if (-not $dockerRunning) { $missing += "a running Docker Desktop (start it and wait until it is ready)" }
}
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    $missing += "Ollama (winget install Ollama.Ollama)"
} elseif (-not (Test-Url "http://127.0.0.1:11434/api/version")) {
    $missing += "a running Ollama (start it from the Start menu)"
}
if ($missing) {
    throw "Missing: `n  - $($missing -join "`n  - ")`nInstall or start these, then run this script again."
}
Write-Host "Git, Python $pythonVersion, Docker and Ollama are ready."

Step "2. Private repository"
$privateRepo = Join-Path (Split-Path -Parent $repository) "knowledge_radar_private"
if (Test-Path (Join-Path $privateRepo ".git")) {
    Write-Host "Found: $privateRepo"
} elseif ($PrivateRepoUrl) {
    Invoke-Checked "git clone" { git clone $PrivateRepoUrl $privateRepo }
} else {
    throw "No private checkout at $privateRepo. Run again with -PrivateRepoUrl <clone URL> (the SSH key for it must be set up)."
}

Step "3. Python environment and git hooks"
$python = Join-Path $repository ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Invoke-Checked "python -m venv" { python -m venv (Join-Path $repository ".venv") }
}
Push-Location $repository
try {
    Invoke-Checked "pip install" { & $python -m pip install --quiet -e ".[dev]" }
    Invoke-Checked "git config" { git config core.hooksPath .githooks }
} finally {
    Pop-Location
}
Write-Host "Package installed in .venv; git hooks enabled."

Step "4. local-config.yaml"
$config = Join-Path $repository "local-config.yaml"
if (Test-Path $config) {
    Write-Host "Exists, left unchanged: $config"
} else {
    $example = Get-Content (Join-Path $repository "local-config.example.yaml") -Raw
    $path = $privateRepo -replace "\\", "/"
    Set-Content -Path $config -Encoding utf8 -Value ($example -replace "(?m)^private_repo_path:.*$", "private_repo_path: $path")
    Write-Host "Written with private_repo_path: $path"
}

Step "5. Ollama models"
foreach ($model in @($ChatModel, $embeddingModel)) {
    Invoke-Checked "ollama pull $model" { ollama pull $model }
}

Step "6. Secrets in the Credential Manager"
foreach ($user in @("neo4j", "neo4j-private", "gitlab")) {
    $secret = & $python -m keyring get knowledge-radar $user
    if ($secret) {
        Write-Host "$user`: stored"
        continue
    }
    if ($user -eq "gitlab") {
        Write-Host "The GitLab token (role Maintainer, scope write_repository) turns on the private inbox in the Review Dashboard."
        $answer = Read-Host "Store it now? (y/N)"
        if ($answer -notmatch "^[yYjJ]") {
            Write-Host "Skipped; later: python -m keyring set knowledge-radar gitlab"
            continue
        }
    } else {
        Write-Host "Choose a new password for the index '$user' (input is hidden)."
    }
    Invoke-Checked "keyring set $user" { & $python -m keyring set knowledge-radar $user }
}

if ($SkipIndex) {
    Step "7. Indices: skipped (-SkipIndex)"
} else {
    Step "7. Indices"
    & (Join-Path $PSScriptRoot "start-neo4j.ps1")
    & (Join-Path $PSScriptRoot "start-neo4j.ps1") -Private
    $deadline = (Get-Date).AddSeconds(120)
    while (-not ((Test-Url "http://127.0.0.1:7474") -and (Test-Url "http://127.0.0.1:7475"))) {
        if ((Get-Date) -gt $deadline) {
            throw "Neo4j did not start within 2 minutes; see: docker compose logs neo4j"
        }
        Start-Sleep -Seconds 3
    }
    # The index commands read both Neo4j passwords from the Credential Manager.
    Push-Location $repository
    try {
        Invoke-Checked "public index" { & $python -m app.backend.knowledge_radar.index }
        Invoke-Checked "private structural graph" { & $python -m app.agents.private_ingest }
        Invoke-Checked "private extraction" { & $python -m app.agents.private_extract --model $ChatModel }
        Invoke-Checked "private index" { & $python -m app.backend.knowledge_radar.private_index }
    } finally {
        Pop-Location
    }
}

Step "8. Start the app"
& (Join-Path $PSScriptRoot "start-app.ps1")
