<#
.SYNOPSIS
    Registers the weekly Knowledge Radar monitoring task for the current user.
.DESCRIPTION
    Fills the machine-specific placeholders in scheduled_task.xml (repository path,
    user) and registers the task with Windows Task Scheduler. Use -DryRun to print
    the resulting XML without registering anything.
#>
[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$template = Get-Content -Raw -Encoding UTF8 (Join-Path $repoRoot "scheduled_task.xml")
$userId = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

$escape = { param($value) [System.Security.SecurityElement]::Escape($value) }
$xml = $template.Replace("{{REPO_ROOT}}", (& $escape $repoRoot)).Replace("{{USER_ID}}", (& $escape $userId))
[xml]$xml | Out-Null  # fail early on malformed XML
# The template declares UTF-8, but Register-ScheduledTask receives a .NET string
# (UTF-16) and rejects the declaration ("unable to switch the encoding").
$xml = $xml -replace '^\s*<\?xml[^>]*\?>\s*', ''

if ($DryRun) {
    $xml
    return
}

Register-ScheduledTask -TaskPath "\Knowledge Radar\" -TaskName "Weekly monitoring" -Xml $xml -Force -ErrorAction Stop | Out-Null
Write-Host "Registered '\Knowledge Radar\Weekly monitoring' for $userId (repository: $repoRoot)."
