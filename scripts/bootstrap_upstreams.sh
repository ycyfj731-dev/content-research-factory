#!/usr/bin/env bash
set -euo pipefail

ROOT="${CRF_VENDOR_DIR:-.vendor}"
mkdir -p "$ROOT"

clone_or_update() {
  local repo="$1"
  local dir="$2"
  local ref="$3"
  if [ -d "$dir/.git" ]; then
    git -C "$dir" fetch --depth 1 origin "$ref"
    git -C "$dir" checkout "$ref"
    git -C "$dir" pull --ff-only origin "$ref"
  else
    git clone --depth 1 --branch "$ref" "$repo" "$dir"
  fi
}

clone_or_update "https://github.com/sansan0/TrendRadar.git" "$ROOT/TrendRadar" master
clone_or_update "https://github.com/Bowenwin/MediaCrawler_MCP_Server.git" "$ROOT/MediaCrawler_MCP_Server" main
clone_or_update "https://github.com/harry0703/MoneyPrinterTurbo.git" "$ROOT/MoneyPrinterTurbo" main

python -m pip install -U "git+https://github.com/Panniantong/Agent-Reach.git"

(cd "$ROOT/TrendRadar" && uv sync)
(cd "$ROOT/MediaCrawler_MCP_Server" && uv sync && uv run playwright install chromium)
(cd "$ROOT/MoneyPrinterTurbo" && uv sync)

echo "Upstreams installed under: $ROOT"
echo "TREND_RADAR_DIR=$ROOT/TrendRadar"
echo "MEDIA_CRAWLER_DIR=$ROOT/MediaCrawler_MCP_Server"
echo "MONEY_PRINTER_TURBO_DIR=$ROOT/MoneyPrinterTurbo"
