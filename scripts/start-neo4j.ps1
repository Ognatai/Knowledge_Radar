# Start the local index (Neo4j Community in Docker, bound to localhost only).
#
# The password is read from the Windows Credential Manager and passed to Docker
# Compose for this process only; it is never written to a file. Store it once with:
#
#     python -m keyring set knowledge-radar neo4j
#
# Neo4j sets the password when the data volume is first created; changing it
# later requires removing the volume (`docker compose down -v`) or changing it
# inside Neo4j.

$ErrorActionPreference = "Stop"
$repository = Split-Path -Parent $PSScriptRoot

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is not installed or not on PATH (see SETUP.md, 'Local index')."
}
$password = python -m keyring get knowledge-radar neo4j
if (-not $password) {
    throw "No Neo4j password in the Credential Manager. Run: python -m keyring set knowledge-radar neo4j"
}

$env:NEO4J_PASSWORD = $password
try {
    docker compose --project-directory $repository up -d neo4j
} finally {
    Remove-Item Env:NEO4J_PASSWORD
}
Write-Host "Neo4j: bolt://127.0.0.1:7687, browser http://127.0.0.1:7474"
