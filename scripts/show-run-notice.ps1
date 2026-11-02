<#
.SYNOPSIS
    Shows the result of the last weekly monitoring run as a window.
.DESCRIPTION
    run-monitoring.ps1 writes .knowledge-radar\monitoring\run-notice.json after every
    run (app.agents.monitoring.notice) and starts the task "\Knowledge Radar\Run
    notice", which runs this script; the task also runs it at logon and when the PC is
    unlocked. The run happens at night, so the window waits on the desktop until the
    PC is woken. The notice is deleted once the window was closed, so a notice lost to
    a restart comes back at the next logon. Without a notice the script does nothing.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$noticeFile = Join-Path $repoRoot ".knowledge-radar\monitoring\run-notice.json"
if (-not (Test-Path $noticeFile)) { exit 0 }

# Logon and unlock may both fire while a window is still open; show it only once.
$mutex = New-Object System.Threading.Mutex($false, "Local\KnowledgeRadarRunNotice")
if (-not $mutex.WaitOne(0)) { exit 0 }
try {
    $notice = Get-Content -Raw -Encoding UTF8 $noticeFile | ConvertFrom-Json
    Add-Type -AssemblyName System.Windows.Forms
    $icon = if ($notice.failed) { [System.Windows.Forms.MessageBoxIcon]::Error } else { [System.Windows.Forms.MessageBoxIcon]::Information }
    # A hidden topmost owner keeps the window in front of everything else.
    $owner = New-Object System.Windows.Forms.Form -Property @{ TopMost = $true; ShowInTaskbar = $false; WindowState = "Minimized" }
    $answer = [System.Windows.Forms.MessageBox]::Show(
        $owner,
        "$($notice.message)`n`nLog öffnen?",
        $notice.title,
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        $icon
    )
    $owner.Dispose()
    Remove-Item -LiteralPath $noticeFile -Force
    if ($answer -eq [System.Windows.Forms.DialogResult]::Yes -and (Test-Path $notice.log)) {
        Start-Process notepad.exe -ArgumentList "`"$($notice.log)`""
    }
}
finally {
    $mutex.ReleaseMutex()
}
