# Start the Ollama tray app with the settings the agent pipeline needs on the Desktop
# (AMD Radeon RX 7900 XT, Windows). The settings apply only to the Ollama processes
# started here; other programs keep their ROCm access.
#
# - Vulkan instead of ROCm: on this GPU, decode speed under ROCm falls from about 110
#   to 18 tokens/s as the context grows to 14k tokens; Vulkan keeps about 30 tokens/s,
#   which made extraction several times faster. Ollama only uses Vulkan when ROCm is
#   hidden from it (HIP_VISIBLE_DEVICES=-1).
# - KV cache q8_0 (requires flash attention): halves the cache, so qwen3:30b-a3b with
#   a 24k context fits completely into the 20 GB VRAM.
#
# Used as the Windows autostart entry for Ollama (see SETUP.md). Running it again
# restarts Ollama with these settings.

param(
    # Seconds to wait first when started at logon, so that this instance replaces one
    # started by Ollama's own autostart entry (restored by updates) instead of racing it.
    [int]$Delay = 0
)

$ErrorActionPreference = "Stop"
$ollamaApp = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama app.exe"
if (-not (Test-Path $ollamaApp)) {
    throw "Ollama is not installed at $ollamaApp"
}

if ($Delay -gt 0) {
    Start-Sleep -Seconds $Delay
}

# Stop any running instance, including model runners that can outlive ollama.exe and
# keep VRAM allocated (the next model load then fails with an out-of-memory error).
foreach ($name in @("ollama app", "ollama", "llama-server")) {
    Get-Process -Name $name -ErrorAction SilentlyContinue | Stop-Process -Force -Confirm:$false
}
Start-Sleep -Seconds 2

$env:OLLAMA_VULKAN = "1"
$env:HIP_VISIBLE_DEVICES = "-1"
$env:OLLAMA_FLASH_ATTENTION = "1"
$env:OLLAMA_KV_CACHE_TYPE = "q8_0"
Start-Process -FilePath $ollamaApp -WorkingDirectory (Split-Path $ollamaApp)

for ($attempt = 0; $attempt -lt 30; $attempt++) {
    Start-Sleep -Seconds 1
    try {
        Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 "http://127.0.0.1:11434/api/version" | Out-Null
        Write-Output "Ollama started with Vulkan and KV cache q8_0."
        exit 0
    } catch {}
}
throw "Ollama did not respond within 30 seconds."
