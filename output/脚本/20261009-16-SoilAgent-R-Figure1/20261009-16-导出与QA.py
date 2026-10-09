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
    assert root.get("width") == "180mm" and root.get("height") == "63mm"
    _, _, view_width, view_height = map(float, root.get("viewBox").split())
    nodes = {node.get("id"): node for node in root.iter() if node.get("id")}
    typography = check_arial(root)

    # CairoSVG保留字体和虚线；PyMuPDF的SVG转换会丢失dash，不能用作本图导出器。
    converted_bytes = cairosvg.svg2pdf(url=str(source))
    with pymupdf.open("pdf", converted_bytes) as document:
        page = document[0]
        document.set_metadata({"title": "SoilAgent-R Figure 1", "author": "Drawing studio", "subject": "Four agent responsibility groups over five tool/model modules; conceptual draft pending review; not verified independent agent runtimes or publication final"})
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
        # 对精简后右侧独立标签，用最终PDF字体度量检查文字碰撞。
        right_labels = ["CONC", "COST", "FLUX", "Outputs", "Plans", "Candidate schemes"]
        right_rects = {label: page.search_for(label) for label in right_labels}
        collisions = []
        for index, first in enumerate(right_labels):
            for second in right_labels[index + 1:]:
                if any((a & b).get_area() > 0.5 for a in right_rects[first] for b in right_rects[second]):
                    collisions.append([first, second])
        def svg_band(left, top, right, bottom):
            return pymupdf.Rect(rect.width * left / view_width, rect.height * top / view_height,
                                rect.width * right / view_width, rect.height * bottom / view_height)

        # 仅在共同标题带查找；画幅高度不参与字体或坐标的缩放。
        header_clip = svg_band(0, 160, view_width, 225)
        header_labels = ["0 Auto-ETL", "1 CSM", "2 Digital twin", "3 RTM", "4 MOPSO"]
        header_rects = {label: page.search_for(label, clip=header_clip) for label in header_labels}
        header_unique = all(len(boxes) == 1 for boxes in header_rects.values())
        header_collisions = []
        for index, first in enumerate(header_labels):
            for second in header_labels[index + 1:]:
                if any((a & b).get_area() > 0.5 for a in header_rects[first] for b in header_rects[second]):
                    header_collisions.append([first, second])
        agent_groups = [n for n in root.iter() if n.get("data-role") == "agent-scope"]
        agent_mappings = {n.get("id"): n.get("data-modules") for n in agent_groups}
        expected_agent_mappings = {"site-agent": "etl,csm", "twin-agent": "twin", "prediction-agent": "rtm", "decision-agent": "decision"}
        agent_rects = {}
        agent_fit = []
        for group in agent_groups:
            label = group.find(NS + "text").text
            frame = group.find(NS + "rect")
            x, y, width, height = (float(frame.get(key)) for key in ["x", "y", "width", "height"])
            frame_rect = svg_band(x, y, x + width, y + height)
            boxes = page.search_for(label)
            agent_rects[label] = boxes
            agent_fit.append(len(boxes) == 1 and frame_rect.contains(boxes[0]))
        top_rects = {**agent_rects, **header_rects,
                     "Research goal / site information": page.search_for("Research goal / site information"),
                     "User revises goals": page.search_for("User revises goals")}
        top_collisions = []
        top_labels = list(top_rects)
        for index, first in enumerate(top_labels):
            for second in top_labels[index + 1:]:
                if any((a & b).get_area() > 0.5 for a in top_rects[first] for b in top_rects[second]):
                    top_collisions.append([first, second])
        visible_text = " ".join(s["text"] for s in spans)
        removed_labels = ["Conceptualization", "Site reconstruction", "Reaction prediction", "Plan optimization", "Color: CONC", "STRUCTURE DRAFT", "Dashed:", "Conceptual illustration / not to scale", "Geometry / initial fields / support", "Time evolution", "Mass checks"]
        allowed_subscripts = sorted(n.text.strip() for n in root.iter(NS + "tspan") if n.get("dy") == "8")
        formula_bands = {"balance": (522, 615)}
        formula_rects = {}
        for name, (top, bottom) in formula_bands.items():
            band = svg_band(1175, top, 1365, bottom)
            members = [s for s in spans if band.contains(pymupdf.Rect(s["bbox"]))]
            if members:
                box = pymupdf.Rect(members[0]["bbox"])
                for member in members[1:]:
                    box |= pymupdf.Rect(member["bbox"])
                formula_rects[name] = box
        formula_collisions = [[name, label] for name, box in formula_rects.items() for label, boxes in right_rects.items() if any((box & other).get_area() > 0.5 for other in boxes)]
        equals_rects = page.search_for("=")
        balance_centered = "balance" in formula_rects and abs(
            (formula_rects["balance"].x0 + formula_rects["balance"].x1) / 2
            - rect.width * float(nodes["rtm-method-label"].get("x")) / view_width
        ) < 0.5
        partition_absent = not any(ident.startswith("rtm-partition") for ident in ids)
        annotation_groups = [nodes[name] for name in ["etl-annotations", "csm-annotations", "twin-parameter-fields", "rtm-equations", "decision-output"]]
        final_baselines = [group.get("data-final-baseline") for group in annotation_groups]
        header_baselines = [node.get("y") for node in root.iter() if node.get("data-role") == "module-title"]
        checks = {
            "svg_unique_ids": True,
            "svg_no_raster_or_filter": True,
            "pdf_single_page": len(document) == 1,
            "pdf_no_image_objects": len(page.get_images(full=True)) == 0,
            "pdf_text_present": len(spans) > 20,
            "pdf_text_inside_page": not clipped,
            "pdf_main_labels_minimum_font_7pt": bool(main_spans) and min(s["size"] for s in main_spans) >= 7.0,
            "pdf_only_native_subscripts_below_7pt": sorted(s["text"].strip() for s in small_spans if s["text"].strip()) == allowed_subscripts and min_font >= 6.0,
            "pdf_arial_bold_no_fallback": all("Arial" in f and "Bold" in f for f in fonts),
            "pdf_dashed_guidance_and_feedback_preserved": dashed_paths >= 2,
            "pdf_right_labels_present_once": all(len(boxes) == 1 for boxes in right_rects.values()),
            "pdf_right_labels_no_text_collision": not collisions,
            "pdf_model_headers_present_once": header_unique,
            "pdf_model_headers_no_text_collision": not header_collisions,
            "svg_four_agent_scopes_cover_five_modules": agent_mappings == expected_agent_mappings and len(agent_groups) == 4,
            "pdf_agent_labels_fit_header_frames": len(agent_fit) == 4 and all(agent_fit),
            "pdf_agent_headers_input_feedback_no_text_collision": not top_collisions,
            "pdf_removed_process_and_figure_notes_absent": all(label not in visible_text for label in removed_labels),
            "svg_shared_footer_and_divider_absent": "shared-resources" not in ids and not any(n.get("d") == "M60 755 L1740 755" for n in root.iter(NS + "path")),
            "pdf_shared_footer_absent": "Shared data / tools" not in visible_text,
            "pdf_rtm_balance_present": set(formula_rects) == set(formula_bands) and bool(page.search_for("dM")) and bool(page.search_for("dt")) and bool(page.search_for("∑F")),
            "pdf_rtm_balance_no_label_collision": not formula_collisions,
            "pdf_rtm_only_one_equation_equals_sign": len(equals_rects) == 1,
            "pdf_rtm_balance_centered_under_header": balance_centered,
            "svg_partition_equation_removed": partition_absent,
            "svg_five_title_baselines_aligned": len(header_baselines) == 5 and set(header_baselines) == {"200"},
            "svg_five_annotation_final_baselines_aligned": final_baselines == ["590"] * 5,
            "svg_compact_bottom_margin": view_height - float(final_baselines[0]) == 40,
            "pdf_conc_axis_replaces_time": len(right_rects["CONC"]) == 1 and "TIME" not in visible_text,
            "pdf_width_180mm": abs(rect.width * 25.4 / 72 - 180) < 0.01,
            "pdf_height_63mm": abs(rect.height * 25.4 / 72 - 63) < 0.01,
        }
        receipt = {
            "stage": "structure_draft_four_agent_scopes_single_rtm_balance",
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
            "model_header_boxes_pt": {label: [list(box) for box in boxes] for label, boxes in header_rects.items()},
            "model_header_collisions": header_collisions,
            "agent_responsibility_mapping": agent_mappings,
            "agent_label_boxes_pt": {label: [list(box) for box in boxes] for label, boxes in agent_rects.items()},
            "top_label_collisions": top_collisions,
            "formula_boxes_pt": {name: list(box) for name, box in formula_rects.items()},
            "formula_label_collisions": formula_collisions,
            "rtm_equal_sign_boxes_pt": [list(box) for box in equals_rects],
            "partition_equation_displayed": not partition_absent,
            "module_title_baselines_svg": header_baselines,
            "module_annotation_final_baselines_svg": final_baselines,
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
