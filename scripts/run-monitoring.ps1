<#
.SYNOPSIS
    Weekly monitoring run (started by Windows Task Scheduler on the Desktop).
.DESCRIPTION
    Starts what the pipeline needs (Docker Desktop, Neo4j, Ollama) if it is not
    running, then runs app.agents.monitoring.weekly: validate the notes, update
    the index, fetch sources, assess relevance, write drafts. Writes a log file to
    .knowledge-radar/logs/ and shows a Windows toast notification with the
    summary; drafts wait in .knowledge-radar/monitoring/drafts/ for review.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$logDirectory = Join-Path $repoRoot ".knowledge-radar\logs"
New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null
$logFile = Join-Path $logDirectory ("monitoring-{0:yyyy-MM-dd_HHmmss}.log" -f (Get-Date))

function Write-Log([string]$message) {
    $line = "{0:yyyy-MM-dd HH:mm:ss}  {1}" -f (Get-Date), $message
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

function Show-Toast([string]$title, [string]$message) {
    try {
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
        $escape = { param($value) [System.Security.SecurityElement]::Escape($value) }
        $toastXml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $toastXml.LoadXml(
            "<toast><visual><binding template='ToastGeneric'>" +
            "<text>$(& $escape $title)</text><text>$(& $escape $message)</text>" +
            "</binding></visual></toast>"
        )
        # Windows PowerShell's registered AppUserModelID, so no app registration is needed.
        $appId = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show(
            [Windows.UI.Notifications.ToastNotification]::new($toastXml)
        )
    }
    catch {
        Write-Log "Toast notification failed: $($_.Exception.Message)"
    }
}

function Wait-Until([scriptblock]$condition, [int]$seconds, [string]$what) {
    $deadline = (Get-Date).AddSeconds($seconds)
    while ((Get-Date) -lt $deadline) {
        if (& $condition) { return }
        Start-Sleep -Seconds 5
    }
    throw "$what did not become ready within $seconds seconds."
}

function Test-Docker {
    $ErrorActionPreference = "Continue"
    docker info --format "{{.ServerVersion}}" 2>$null | Out-Null
    return $LASTEXITCODE -eq 0
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

$python = Join-Path $repoRoot ".venv\Scripts\python.exe"
try {
    Set-Location $repoRoot
    if (-not (Test-Path $python)) {
        throw "Python virtual environment not found at $python (see SETUP.md)."
    }
    Write-Log "Monitoring run started in $repoRoot."

    if (-not (Test-Docker)) {
        # docker.exe lives in <Docker Desktop>\resources\bin.
        $dockerCli = (Get-Command docker -ErrorAction Stop).Source
        $dockerDesktop = Join-Path (Split-Path (Split-Path (Split-Path $dockerCli))) "Docker Desktop.exe"
        Write-Log "Starting Docker Desktop ($dockerDesktop)."
        Start-Process -FilePath $dockerDesktop
        Wait-Until { Test-Docker } 300 "Docker"
    }
    Write-Log "Starting Neo4j."
    & (Join-Path $PSScriptRoot "start-neo4j.ps1") *>&1 | ForEach-Object { Write-Log "$_" }
    Wait-Until { Test-Url "http://127.0.0.1:7474" } 180 "Neo4j"

    if (-not (Test-Url "http://127.0.0.1:11434/api/version")) {
        Write-Log "Starting Ollama."
        & (Join-Path $PSScriptRoot "start-ollama.ps1") *>&1 | ForEach-Object { Write-Log "$_" }
        Wait-Until { Test-Url "http://127.0.0.1:11434/api/version" } 120 "Ollama"
    }

    # Python's output is UTF-8; without this, Windows PowerShell decodes it with the OEM code page.
    $env:PYTHONIOENCODING = "utf-8"
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $summary = "no summary"
    # Python writes progress to stderr too; Windows PowerShell must not treat it as an error.
    $ErrorActionPreference = "Continue"
    & $python -u -m app.agents.monitoring.weekly 2>&1 | ForEach-Object {
        $line = "$_"
        if ($line.StartsWith("SUMMARY: ")) { $summary = $line.Substring(9) }
        Write-Log $line
    }
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = "Stop"
    if ($exitCode -ne 0) {
        throw "$summary"
    }

    Write-Log "Monitoring run finished successfully."
    Show-Toast "Knowledge Radar: weekly run finished" "$summary Log: $logFile"
    exit 0
}
catch {
    Write-Log "Monitoring run FAILED: $($_.Exception.Message)"
    Show-Toast "Knowledge Radar: weekly run failed" "$($_.Exception.Message) Log: $logFile"
    exit 1
}
