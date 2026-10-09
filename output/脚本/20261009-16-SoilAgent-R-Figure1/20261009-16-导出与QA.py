"""导出原创 SVG 草图为矢量 PDF/PNG，并生成技术检查回执。"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import cairosvg
from fontTools.ttLib import TTFont
import pymupdf

THEME = "20261009-16-SoilAgent-R-Figure1"
STEM = "20261009-16-系统架构-结构草图"
NS = "{http://www.w3.org/2000/svg}"


def check_arial(root: ET.Element) -> dict:
    """缺真正Arial Bold或缺字符就报错，不静默替换为Liberation/DejaVu。"""
    resolved = subprocess.run(
        ["fc-match", "-f", "%{file}", "Arial:style=Bold"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    with TTFont(resolved) as font:
        family = font["name"].getDebugName(1)
        face = font["name"].getDebugName(2)
        if family != "Arial" or face != "Bold":
            raise RuntimeError(f"需要真正Arial Bold，当前匹配为 {family} / {face}")
        visible = "".join("".join(n.itertext()) for n in root.iter(NS + "text"))
        cmap = font.getBestCmap()
        missing = sorted({ch for ch in visible if not ch.isspace() and ord(ch) not in cmap})
        if missing:
            raise RuntimeError(f"Arial Bold缺字符：{missing}；请用可编辑tspan实现上下标")
        return {
            "style": "yyc_typography_only",
            "requested_family": "Arial",
            "requested_face": "Bold",
            "resolved_family": family,
            "resolved_face": face,
            "font_filename": Path(resolved).name,
            "font_sha256": hashlib.sha256(Path(resolved).read_bytes()).hexdigest(),
            "font_version": font["name"].getDebugName(5),
            "font_embedding_fstype": font["OS/2"].fsType,
            "missing_visible_glyphs": missing,
        }


def export(repo: Path) -> dict:
    figures = repo / "output" / "图" / THEME
    reports = repo / "output" / "报告" / THEME
    source = figures / f"{STEM}.svg"
    root = ET.parse(source).getroot()
    ids = [node.get("id") for node in root.iter() if node.get("id")]
    assert len(ids) == len(set(ids)), "SVG ID 重复"
    forbidden = {"image", "script", "foreignObject", "filter", "linearGradient", "radialGradient"}
    assert not any(n.tag.removeprefix(NS) in forbidden for n in root.iter()), "SVG含禁用元素"
    assert root.get("width") == "180mm" and root.get("height") == "82mm"
    typography = check_arial(root)

    # CairoSVG保留字体和虚线；PyMuPDF的SVG转换会丢失dash，不能用作本图导出器。
    converted_bytes = cairosvg.svg2pdf(url=str(source))
    with pymupdf.open("pdf", converted_bytes) as document:
        page = document[0]
        document.set_metadata({"title": "SoilAgent-R Figure 1 — structure draft", "author": "Drawing studio", "subject": "Conceptual illustration; RTM/Decision layout revision; not publication final"})
        document.save(figures / f"{STEM}.pdf", garbage=4, deflate=True)
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(4, 4), alpha=False)
        pixmap.save(figures / f"{STEM}.png")

    with pymupdf.open(figures / f"{STEM}.pdf") as document:
        page = document[0]
        spans = [s for b in page.get_text("dict")["blocks"] if "lines" in b for line in b["lines"] for s in line["spans"]]
        rect = page.rect
        clipped = [s["text"] for s in spans if not rect.contains(pymupdf.Rect(s["bbox"]))]
        min_font = min(s["size"] for s in spans)
        main_spans = [s for s in spans if s["size"] >= 7.0]
        small_spans = [s for s in spans if s["size"] < 7.0]
        drawings = page.get_drawings()
        dashed_paths = sum(bool(d.get("dashes")) and not d["dashes"].startswith("[]") for d in drawings)
        fonts = sorted({s["font"] for s in spans})
        # 对本轮右侧整理的六个独立标签，用最终PDF字体度量检查文字碰撞。
        right_labels = ["Time evolution", "Mass checks", "Color: CONC", "Outputs", "Plans", "Candidate schemes"]
        right_rects = {label: page.search_for(label) for label in right_labels}
        collisions = []
        for index, first in enumerate(right_labels):
            for second in right_labels[index + 1:]:
                if any((a & b).get_area() > 0.5 for a in right_rects[first] for b in right_rects[second]):
                    collisions.append([first, second])
        checks = {
            "svg_unique_ids": True,
            "svg_no_raster_or_filter": True,
            "pdf_single_page": len(document) == 1,
            "pdf_no_image_objects": len(page.get_images(full=True)) == 0,
            "pdf_text_present": len(spans) > 20,
            "pdf_text_inside_page": not clipped,
            "pdf_main_labels_minimum_font_7pt": bool(main_spans) and min(s["size"] for s in main_spans) >= 7.0,
            "pdf_only_time_subscripts_below_7pt": len(small_spans) == 2 and {s["text"].strip() for s in small_spans} == {"0", "1"} and min_font >= 6.0,
            "pdf_arial_bold_no_fallback": all("Arial" in f and "Bold" in f for f in fonts),
            "pdf_dashed_guidance_and_feedback_preserved": dashed_paths >= 2,
            "pdf_right_labels_present_once": all(len(boxes) == 1 for boxes in right_rects.values()),
            "pdf_right_labels_no_text_collision": not collisions,
            "pdf_width_180mm": abs(rect.width * 25.4 / 72 - 180) < 0.01,
            "pdf_height_82mm": abs(rect.height * 25.4 / 72 - 82) < 0.01,
        }
        receipt = {
            "stage": "structure_draft_right_side_layout_revision",
            "source": source.relative_to(repo).as_posix(),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "backend": f"CairoSVG {cairosvg.__version__}; PyMuPDF {pymupdf.VersionBind} for PDF QA/render",
            "typography": typography,
            "checks": checks,
            "pdf_width_mm": rect.width * 25.4 / 72,
            "pdf_height_mm": rect.height * 25.4 / 72,
            "pdf_minimum_font_pt": min_font,
            "pdf_main_label_minimum_font_pt": min(s["size"] for s in main_spans),
            "pdf_text_spans": len(spans),
            "pdf_vector_drawings": len(drawings),
            "pdf_fonts": fonts,
            "pdf_dashed_paths": dashed_paths,
            "pdf_image_objects": len(page.get_images(full=True)),
            "clipped_text": clipped,
            "right_label_boxes_pt": {label: [list(box) for box in boxes] for label, boxes in right_rects.items()},
            "right_label_collisions": collisions,
            "png_size_pixels": [pixmap.width, pixmap.height],
            "not_checked_by_this_script": ["visual_layout", "scientific_acceptance", "drawio_desktop_export", "journal_specific_submission_rules"],
        }
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "20261009-16-结构草图-QA.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not all(checks.values()):
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    print(json.dumps(export(parser.parse_args().repo.resolve()), ensure_ascii=False, indent=2))
