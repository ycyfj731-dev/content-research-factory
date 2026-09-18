$ErrorActionPreference = "Stop"

$Root = if ($env:CRF_VENDOR_DIR) { $env:CRF_VENDOR_DIR } else { ".vendor" }
New-Item -ItemType Directory -Force -Path $Root | Out-Null

function Sync-Repo($Repo, $Dir, $Ref) {
    if (Test-Path (Join-Path $Dir ".git")) {
        git -C $Dir fetch --depth 1 origin $Ref
        git -C $Dir checkout $Ref
        git -C $Dir pull --ff-only origin $Ref
    } else {
        git clone --depth 1 --branch $Ref $Repo $Dir
    }
}

$Trend = Join-Path $Root "TrendRadar"
$Media = Join-Path $Root "MediaCrawler_MCP_Server"
$Money = Join-Path $Root "MoneyPrinterTurbo"

Sync-Repo "https://github.com/sansan0/TrendRadar.git" $Trend "master"
Sync-Repo "https://github.com/Bowenwin/MediaCrawler_MCP_Server.git" $Media "main"
Sync-Repo "https://github.com/harry0703/MoneyPrinterTurbo.git" $Money "main"

python -m pip install -U "git+https://github.com/Panniantong/Agent-Reach.git"

Push-Location $Trend
uv sync
Pop-Location

Push-Location $Media
uv sync
uv run playwright install chromium
Pop-Location

Push-Location $Money
uv sync
Pop-Location

$env:TREND_RADAR_DIR = (Resolve-Path $Trend).Path
$env:MEDIA_CRAWLER_DIR = (Resolve-Path $Media).Path
$env:MONEY_PRINTER_TURBO_DIR = (Resolve-Path $Money).Path

Write-Host "Upstreams installed."
Write-Host "TREND_RADAR_DIR=$env:TREND_RADAR_DIR"
Write-Host "MEDIA_CRAWLER_DIR=$env:MEDIA_CRAWLER_DIR"
Write-Host "MONEY_PRINTER_TURBO_DIR=$env:MONEY_PRINTER_TURBO_DIR"
Write-Host ""
Write-Host "These environment variables are set for the current PowerShell session."
