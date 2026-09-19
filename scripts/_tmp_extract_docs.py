"""Extrai texto de .docx/.xlsx usando apenas a stdlib (zip + XML).

Uso: python scripts/_tmp_extract_docs.py
Saída: .kiro/_extracted/<nome>.md
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".kiro" / "_extracted"


def para_text(p: ET.Element) -> str:
    parts: list[str] = []
    for node in p.iter():
        if node.tag == f"{W}t":
            parts.append(node.text or "")
        elif node.tag in (f"{W}tab",):
            parts.append("\t")
        elif node.tag in (f"{W}br", f"{W}cr"):
            parts.append("\n")
    return "".join(parts).strip()


def para_style(p: ET.Element) -> str:
    pr = p.find(f"{W}pPr")
    if pr is None:
        return ""
    st = pr.find(f"{W}pStyle")
    if st is None:
        return ""
    return st.get(f"{W}val") or ""


def render_block(el: ET.Element, out: list[str]) -> None:
    if el.tag == f"{W}p":
        txt = para_text(el)
        if not txt:
            return
        style = para_style(el)
        m = re.match(r"(?:Heading|Titulo|Ttulo|Título)(\d)", style, re.I)
        if m:
            level = min(int(m.group(1)), 6)
            out.append(f"\n{'#' * level} {txt}\n")
        elif style.lower().startswith("list"):
            out.append(f"- {txt}")
        else:
            out.append(txt)
    elif el.tag == f"{W}tbl":
        rows: list[list[str]] = []
        for tr in el.findall(f"{W}tr"):
            cells: list[str] = []
            for tc in tr.findall(f"{W}tc"):
                cell_txt = " ".join(
                    t for t in (para_text(p) for p in tc.findall(f"{W}p")) if t
                )
                cells.append(cell_txt.replace("|", "\\|"))
            rows.append(cells)
        if not rows:
            return
        width = max(len(r) for r in rows)
        out.append("")
        for i, r in enumerate(rows):
            r = r + [""] * (width - len(r))
            out.append("| " + " | ".join(r) + " |")
            if i == 0:
                out.append("|" + "---|" * width)
        out.append("")


def extract_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    tree = ET.fromstring(xml)
    body = tree.find(f"{W}body")
    out: list[str] = []
    if body is not None:
        for el in body:
            render_block(el, out)
    return "\n".join(out)


def col_index(ref: str) -> int:
    letters = re.match(r"([A-Z]+)", ref)
    if not letters:
        return 0
    n = 0
    for ch in letters.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def extract_xlsx(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sst.findall(f"{S}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{S}t")))

        names: dict[str, str] = {}
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rel_map = {
            r.get("Id"): r.get("Target")
            for r in rels
        }
        for sheet in wb.iter(f"{S}sheet"):
            rid = sheet.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )
            target = rel_map.get(rid, "")
            if target and not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")
            names[target] = sheet.get("name") or rid

        out: list[str] = []
        for target, name in names.items():
            if target not in z.namelist():
                continue
            out.append(f"\n## Planilha: {name}\n")
            ws = ET.fromstring(z.read(target))
            for row in ws.iter(f"{S}row"):
                cells: dict[int, str] = {}
                for c in row.findall(f"{S}c"):
                    ref = c.get("r") or ""
                    idx = col_index(ref)
                    t = c.get("t")
                    v = c.find(f"{S}v")
                    isel = c.find(f"{S}is")
                    f = c.find(f"{S}f")
                    if t == "s" and v is not None:
                        try:
                            val = shared[int(v.text or "0")]
                        except (ValueError, IndexError):
                            val = ""
                    elif t == "inlineStr" and isel is not None:
                        val = "".join(x.text or "" for x in isel.iter(f"{S}t"))
                    elif v is not None:
                        val = v.text or ""
                    else:
                        val = ""
                    if f is not None and f.text:
                        val = f"{val} [={f.text}]" if val else f"[={f.text}]"
                    if val.strip():
                        cells[idx] = val.strip().replace("|", "\\|")
                if not cells:
                    continue
                width = max(cells) + 1
                line = [cells.get(i, "") for i in range(width)]
                out.append("| " + " | ".join(line) + " |")
        return "\n".join(out)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    docs = ROOT / "docs"
    files = sorted(
        [p for p in docs.rglob("*") if p.suffix.lower() in {".docx", ".xlsx"}]
    )
    if not files:
        print("nenhum arquivo encontrado")
        return 1
    for p in files:
        try:
            text = extract_docx(p) if p.suffix.lower() == ".docx" else extract_xlsx(p)
        except Exception as exc:  # noqa: BLE001
            print(f"FALHA  {p.name}: {exc}")
            continue
        dest = OUT / (p.stem + ".md")
        dest.write_text(f"# {p.stem}\n\n{text}\n", encoding="utf-8")
        print(f"OK     {p.name} -> {dest.name} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
