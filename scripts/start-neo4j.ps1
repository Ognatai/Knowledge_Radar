# Start the local index (Neo4j Community in Docker, bound to localhost only).
#
# The password is read from the Windows Credential Manager and passed to Docker
# Compose for this process only; it is never written to a file. Store it once with:
#
#     python -m keyring set knowledge-radar neo4j
#
# -Private starts the separate private index instead (own container, volume and
# password; bolt port 7688). It holds the private repository only and is used by
# the chat on the ThinkPad, never by the monitoring pipeline. Its password:
#
#     python -m keyring set knowledge-radar neo4j-private
#
# Neo4j sets the password when the data volume is first created; changing it
# later requires removing the volume (`docker compose down -v`) or changing it
# inside Neo4j.

param(
    [switch]$Private
)

$ErrorActionPreference = "Stop"
$repository = Split-Path -Parent $PSScriptRoot

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is not installed or not on PATH (see SETUP.md, 'Local index')."
}
# The repository's virtual environment has keyring even when it is not activated.
$python = Join-Path $repository ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}
if ($Private) {
    $user, $variable, $service, $ports = "neo4j-private", "NEO4J_PRIVATE_PASSWORD", "neo4j-private", "bolt://127.0.0.1:7688, browser http://127.0.0.1:7475"
} else {
    $user, $variable, $service, $ports = "neo4j", "NEO4J_PASSWORD", "neo4j", "bolt://127.0.0.1:7687, browser http://127.0.0.1:7474"
}
$password = & $python -m keyring get knowledge-radar $user
if (-not $password) {
    throw "No password for '$user' in the Credential Manager. Run: python -m keyring set knowledge-radar $user"
}

Set-Item -Path "Env:$variable" -Value $password
try {
    # Docker reports progress on stderr; Windows PowerShell would treat that as an error.
    $ErrorActionPreference = "Continue"
    if ($Private) {
        docker compose --project-directory $repository -f (Join-Path $repository "docker-compose.private.yml") up -d $service
    } else {
        docker compose --project-directory $repository up -d $service
    }
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose failed with exit code $LASTEXITCODE"
    }
} finally {
    Remove-Item "Env:$variable"
}
Write-Host "Neo4j ($service): $ports"
