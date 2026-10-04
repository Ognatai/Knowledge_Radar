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

if ($DryRun) {
    $xml
    return
}

Register-ScheduledTask -TaskPath "\Knowledge Radar\" -TaskName "Weekly monitoring" -Xml $xml -Force | Out-Null
Write-Host "Registered '\Knowledge Radar\Weekly monitoring' for $userId (repository: $repoRoot)."
