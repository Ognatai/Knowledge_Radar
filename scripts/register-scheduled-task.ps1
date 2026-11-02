<#
.SYNOPSIS
    Registers the weekly Knowledge Radar monitoring task and its result window for the current user.
.DESCRIPTION
    Fills the machine-specific placeholders in scheduled_task.xml (the weekly run) and
    scheduled_task_notice.xml (the window with its result, shown after the run and at
    logon and unlock) and registers both with Windows Task Scheduler. Use -DryRun to
    print the resulting XML without registering anything.
#>
[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$userId = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$escape = { param($value) [System.Security.SecurityElement]::Escape($value) }

foreach ($task in @(
    @{ Name = "Weekly monitoring"; Template = "scheduled_task.xml" },
    @{ Name = "Run notice"; Template = "scheduled_task_notice.xml" }
)) {
    $template = Get-Content -Raw -Encoding UTF8 (Join-Path $repoRoot $task.Template)
    $xml = $template.Replace("{{REPO_ROOT}}", (& $escape $repoRoot)).Replace("{{USER_ID}}", (& $escape $userId))
    [xml]$xml | Out-Null  # fail early on malformed XML
    # The template declares UTF-8, but Register-ScheduledTask receives a .NET string
    # (UTF-16) and rejects the declaration ("unable to switch the encoding").
    $xml = $xml -replace '^\s*<\?xml[^>]*\?>\s*', ''

    if ($DryRun) {
        $xml
        continue
    }

    Register-ScheduledTask -TaskPath "\Knowledge Radar\" -TaskName $task.Name -Xml $xml -Force -ErrorAction Stop | Out-Null
    Write-Host "Registered '\Knowledge Radar\$($task.Name)' for $userId (repository: $repoRoot)."
}
