"""Export the full Kiro CLI session log (.jsonl) to a readable text transcript."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

SESSION_ID = "06ebb9e7-6df7-43be-81fd-2638f3f36ee3"
SRC = Path(os.environ["USERPROFILE"]) / ".kiro" / "sessions" / "cli" / f"{SESSION_ID}.jsonl"
OUT = Path(__file__).resolve().parents[1] / "kiro_full_session.txt"

TOOL_CAP = 6000  # max chars per tool result / thinking block


def cap(text: str, limit: int = TOOL_CAP) -> str:
    text = str(text)
    if len(text) > limit:
        return text[:limit] + f"\n... [truncated {len(text) - limit} chars]"
    return text


def render_block(block: dict) -> list[str]:
    """Render one content block of an AssistantMessage."""
    kind = block.get("kind")
    data = block.get("data")
    if kind == "text":
        return ["ASSISTANT:", str(data), ""]
    if kind == "thinking":
        txt = data.get("text", "") if isinstance(data, dict) else str(data)
        return ["ASSISTANT (thinking):", cap(txt), ""]
    if kind == "toolUse":
        name = data.get("name", "?") if isinstance(data, dict) else "?"
        inp = data.get("input") if isinstance(data, dict) else None
        return [f"ASSISTANT -> tool call: {name}", cap(json.dumps(inp, indent=2)), ""]
    return [f"ASSISTANT [{kind}]:", cap(json.dumps(data)), ""]


def render_tool_result(item: dict) -> list[str]:
    data = item.get("data", {})
    parts: list[str] = []
    for c in data.get("content", []) if isinstance(data, dict) else []:
        ck, cd = c.get("kind"), c.get("data")
        parts.append(cd if ck == "text" else json.dumps(cd))
    status = data.get("status", "") if isinstance(data, dict) else ""
    return [f"TOOL RESULT ({status}):", cap("\n".join(parts)), ""]


def main() -> None:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    out: list[str] = [
        "=" * 80,
        "Bluestock MF Capstone - Full Kiro CLI Session Transcript",
        f"Session ID : {SESSION_ID}",
        f"Exported   : {datetime.now().isoformat(timespec='seconds')}",
        f"Entries    : {len(lines)}",
        "=" * 80,
        "",
    ]
    for i, ln in enumerate(lines, 1):
        entry = json.loads(ln)
        kind = entry.get("kind")
        data = entry.get("data", {})
        out.append(f"\n----- [{i:03d}] {kind} -----")
        if kind == "Prompt":
            for c in data.get("content", []):
                if c.get("kind") == "text":
                    out += ["USER:", str(c.get("data", "")), ""]
        elif kind == "AssistantMessage":
            for c in data.get("content", []):
                out += render_block(c)
        elif kind == "ToolResults":
            for c in data.get("content", []):
                out += render_tool_result(c)
        else:
            out.append(cap(json.dumps(data)))

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes, {len(lines)} entries)")


if __name__ == "__main__":
    main()
