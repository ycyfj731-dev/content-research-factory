from __future__ import annotations

from pathlib import Path

from .models import ResearchPackage


def write_brief(package: ResearchPackage, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Research Brief: {package.query}",
        "",
        "## Summary",
        "",
        f"- Discoveries: {package.synthesis.get('discovery_count', 0)}",
        f"- Cross-platform verifications: {package.synthesis.get('verification_count', 0)}",
        f"- Chinese-social deep research items: {package.synthesis.get('deep_research_count', 0)}",
        f"- Comments collected: {package.synthesis.get('comment_count', 0)}",
        f"- Verified source count: {package.synthesis.get('verified_source_count', 0)}",
        f"- Ready for production: {package.synthesis.get('ready_for_production', False)}",
        "",
        "## Platform coverage",
        "",
    ]

    platform_counts = package.synthesis.get("platform_counts", {})
    if platform_counts:
        for platform, count in sorted(platform_counts.items()):
            lines.append(f"- {platform}: {count}")
    else:
        lines.append("- No platform coverage recorded.")

    lines.extend(["", "## Deep research", ""])
    if package.deep_research:
        for item in package.deep_research:
            label = item.title or item.text or item.source_id or "Untitled item"
            lines.append(f"### {label}")
            lines.append("")
            if item.platform:
                lines.append(f"- Platform: {item.platform}")
            if item.author:
                lines.append(f"- Author: {item.author}")
            if item.url:
                lines.append(f"- URL: {item.url}")
            lines.append(f"- Comments: {len(item.comments)}")
            lines.append("")
    else:
        lines.append("No deep-research items.")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
