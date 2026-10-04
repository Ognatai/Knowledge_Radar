<#
.SYNOPSIS
    Weekly monitoring run (started by Windows Task Scheduler on the Desktop).
.DESCRIPTION
    Writes a log file to .knowledge-radar/logs/ and shows a Windows toast
    notification on success and on failure. Until the LangGraph agent pipeline
    exists (milestone 5), the run validates the public notes only.
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

$python = Join-Path $repoRoot ".venv\Scripts\python.exe"
try {
    Set-Location $repoRoot
    if (-not (Test-Path $python)) {
        throw "Python virtual environment not found at $python (see SETUP.md)."
    }
    Write-Log "Monitoring run started in $repoRoot."

    $output = & $python -m app.agents.validate_notes 2>&1
    $output | ForEach-Object { Write-Log "$_" }
    if ($LASTEXITCODE -ne 0) {
        throw "Note validation failed with exit code $LASTEXITCODE."
    }

    Write-Log "Monitoring run finished successfully."
    Show-Toast "Knowledge Radar: weekly run finished" "Public notes validated. The agent pipeline does not create proposals yet. Log: $logFile"
    exit 0
}
catch {
    Write-Log "Monitoring run FAILED: $($_.Exception.Message)"
    Show-Toast "Knowledge Radar: weekly run failed" "$($_.Exception.Message) Log: $logFile"
    exit 1
}
