#!/usr/bin/env python3
"""Audit the original Lidman--Piccirillo Figure 1 source.

This checker reads only the immutable arXiv:2505.14387v1 source files
``main.tex`` and ``morecurves.pdf``.  It neither imports nor reads Wuebben's
paper, the simplicial fiber/bundle model, correspondence code, or earlier
certificates.  Poppler converts the original vector PDF to SVG and
ImageMagick rasterizes separated vector layers for an intersection audit.
"""

import argparse
import ast
import hashlib
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "main.tex": "183f91362b748f7d633bfd12553ee5abb47ba6835607753eecb4bf04e385dcca",
    "morecurves.pdf": "40ec26c50b735e9f8a3303dd559d668af5abb45d5b78d2c39c30665156963cca",
}
DARK_BLUE = "rgb(38.822937%, 49.01886%, 58.039856%)"
GREEN = "rgb(68.235779%, 73.725891%, 49.01886%)"
SVG_NS = "{http://www.w3.org/2000/svg}"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text):
    return re.sub(r"[^A-Za-z0-9,.\[\]=_-]", "", text).lower()


def source_audit():
    path = Path(__file__)
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
    allowed = {"argparse", "ast", "hashlib", "json", "re", "subprocess",
               "tempfile", "xml.etree.ElementTree", "pathlib"}
    assert imports <= allowed
    return {"sha256": digest(path), "stdlib_imports": sorted(imports),
            "project_imports": []}


def subpaths(data):
    starts = [match.start() for match in re.finditer(r"\bM\b", data)]
    return [data[start:(starts[index + 1] if index + 1 < len(starts)
                        else len(data))].strip()
            for index, start in enumerate(starts)]


def bbox(data):
    numbers = [float(item) for item in
               re.findall(r"-?\d+(?:\.\d+)?", data)]
    assert len(numbers) % 2 == 0 and numbers
    xs, ys = numbers[0::2], numbers[1::2]
    return [min(xs), min(ys), max(xs), max(ys)]


def dimensions(box):
    return box[2] - box[0], box[3] - box[1]


def path_record(path):
    pieces = subpaths(path.attrib["d"])
    return {"element": path, "pieces": pieces, "bbox": bbox(path.attrib["d"]),
            "piece_bboxes": [bbox(piece) for piece in pieces]}


def make_svg(width, height, records):
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">']
    for record, selected in records:
        pieces = record["pieces"]
        data = " ".join(pieces if selected is None
                        else [pieces[index] for index in selected])
        body.append(f'<path fill="white" fill-rule="nonzero" d="{data}"/>')
    body.append("</svg>")
    return "\n".join(body)


def render_mask(svg, width, height, directory, name):
    path = directory / f"{name}.svg"
    path.write_text(svg, encoding="ascii")
    command = ["magick", "-background", "none", str(path),
               "-alpha", "extract", "-threshold", "50%", "-depth", "8",
               "gray:-"]
    raw = subprocess.run(command, check=True, stdout=subprocess.PIPE).stdout
    assert len(raw) == width * height
    return {(index % width, index // width)
            for index, value in enumerate(raw) if value > 127}


def components(points):
    unseen, output = set(points), []
    while unseen:
        start = unseen.pop()
        component, queue = {start}, [start]
        while queue:
            x, y = queue.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    candidate = (x + dx, y + dy)
                    if candidate in unseen:
                        unseen.remove(candidate)
                        component.add(candidate)
                        queue.append(candidate)
        output.append(component)
    return output


def point_bbox(points):
    return [min(x for x, _ in points), min(y for _, y in points),
            max(x for x, _ in points), max(y for _, y in points)]


def close(value, target, tolerance):
    return abs(value - target) <= tolerance


def point_box_distance(point, box):
    x, y = point
    dx = max(box[0] - x, 0, x - box[2])
    dy = max(box[1] - y, 0, y - box[3])
    return (dx * dx + dy * dy) ** .5


def classify_vector_paths(svg_path, directory):
    root = ET.parse(svg_path).getroot()
    width = int(float(root.attrib["width"].removesuffix("pt")))
    height = int(float(root.attrib["height"].removesuffix("pt")))
    assert (width, height) == (1008, 612)
    paths = root.findall(f".//{SVG_NS}path")
    dark = [path_record(path) for path in paths
            if path.attrib.get("fill") == DARK_BLUE]
    green = [path_record(path) for path in paths
             if path.attrib.get("fill") == GREEN]
    assert len(dark) == 7 and len(green) == 1

    large = [record for record in dark
             if 240 < dimensions(record["bbox"])[0] < 270 and
             250 < dimensions(record["bbox"])[1] < 280 and
             len(record["pieces"]) == 3]
    assert len(large) == 2
    large.sort(key=lambda record: record["bbox"][0])
    left, right = large

    vertical_dashes = [record for record in dark
                        if len(record["pieces"]) == 14]
    assert len(vertical_dashes) == 2
    vertical_dashes.sort(key=lambda record: record["bbox"][0])
    a_dash, e_dash = vertical_dashes

    c_solid_candidates = [record for record in dark
                          if len(record["pieces"]) == 1 and
                          dimensions(record["bbox"])[0] > 280]
    assert len(c_solid_candidates) == 1
    c_solid = c_solid_candidates[0]
    c_dashes = [record for record in dark
                if len(record["pieces"]) in (19, 20)]
    assert len(c_dashes) == 2

    layers = {
        "a_solid": [(left, [2])], "a_dashed": [(a_dash, None)],
        "b": [(left, [0, 1])],
        "c_solid": [(c_solid, None)],
        "c_dashed": [(record, None) for record in c_dashes],
        "d": [(right, [0, 1])],
        "e_solid": [(right, [2])], "e_dashed": [(e_dash, None)],
    }
    masks = {name: render_mask(make_svg(width, height, records), width,
                               height, directory, name)
             for name, records in layers.items()}
    full = {
        "a": masks["a_solid"] | masks["a_dashed"],
        "b": masks["b"],
        "c": masks["c_solid"] | masks["c_dashed"],
        "d": masks["d"],
        "e": masks["e_solid"] | masks["e_dashed"],
    }

    true_pairs = {
        "ab": (masks["a_solid"], masks["b"]),
        "bc": (masks["b"], masks["c_solid"]),
        "cd": (masks["c_solid"], masks["d"]),
        "de": (masks["d"], masks["e_solid"]),
    }
    projected_hidden = {
        "ab": (masks["a_dashed"], masks["b"]),
        "bc": (masks["b"], masks["c_dashed"]),
        "cd": (masks["c_dashed"], masks["d"]),
        "de": (masks["d"], masks["e_dashed"]),
    }
    intersections = {}
    for pair, (first, second) in true_pairs.items():
        overlap = first & second
        pieces = components(overlap)
        assert len(pieces) == 1
        hidden_overlap = projected_hidden[pair][0] & projected_hidden[pair][1]
        all_hidden_pieces = components(hidden_overlap)
        hidden_pieces = [piece for piece in all_hidden_pieces if len(piece) >= 2]
        if len(hidden_pieces) != 1:
            raise AssertionError((pair, "hidden projection components",
                                  len(hidden_pieces),
                                  [point_bbox(piece) for piece in hidden_pieces]))
        intersections[pair] = {
            "visible_surface_crossing_components": 1,
            "visible_overlap_pixels": len(overlap),
            "visible_bbox": point_bbox(overlap),
            "dashed_projection_overlap_components_excluded": 1,
            "dashed_overlap_pixels": len(hidden_overlap),
            "single_pixel_antialias_components_ignored": sum(
                len(piece) for piece in all_hidden_pieces if len(piece) < 2),
        }

    nonconsecutive = {}
    for pair in ("ac", "ad", "ae", "bd", "be", "ce"):
        overlap = full[pair[0]] & full[pair[1]]
        assert not overlap
        nonconsecutive[pair] = 0

    # The green vector layer has two clusters of circular subpaths at the two
    # intersections of the rotation axis with the surface.  Each dot is
    # stored as three nested outline subpaths in the source PDF.
    dot_boxes = [box for box in green[0]["piece_bboxes"]
                 if 10 < dimensions(box)[0] < 25 and
                 10 < dimensions(box)[1] < 25]
    assert len(dot_boxes) == 6
    centers = [((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
               for box in dot_boxes]
    top = [point for point in centers if point[1] < height / 2]
    bottom = [point for point in centers if point[1] > height / 2]
    assert len(top) == len(bottom) == 3
    top_center = [sum(point[index] for point in top) / 3 for index in (0, 1)]
    bottom_center = [sum(point[index] for point in bottom) / 3
                     for index in (0, 1)]
    assert close(top_center[0], bottom_center[0], 1)
    assert close(top_center[0], 487, 2)
    assert close(top_center[1], 118, 2)
    assert close(bottom_center[1], 514, 2)

    boxes = {name: point_bbox(mask) for name, mask in full.items()}
    return {
        "svg_dimensions": [width, height],
        "dark_blue_vector_elements": len(dark),
        "curve_pixel_bboxes": boxes,
        "surface_intersections": intersections,
        "nonconsecutive_overlap_pixels": nonconsecutive,
        "fixed_point_dots": {
            "count": 2,
            "top_center": [round(value, 3) for value in top_center],
            "bottom_center": [round(value, 3) for value in bottom_center],
            "common_axis_x": round((top_center[0] + bottom_center[0]) / 2, 3),
        },
        "dash_semantics": (
            "dashed vector pieces are hidden-side projections; only the "
            "solid-solid component is a surface crossing"),
    }


def extract_tex_facts(tex):
    compact = normalize(tex)
    required = [
        "includegraphics[scale=0.2]{morecurves.pdf}",
        "curvesa,b,c,d,econfiguredasinFigure",
        "exchangesaande,bandd,andfixesc",
        "thetwofixedpointsofphiinF",
        "phifixescsetwiseandwithorientation",
    ]
    for token in required:
        assert normalize(token) in compact
    labels = {}
    pattern = re.compile(
        r"\\draw(?:\[[^]]*\])?\s*\(([-\d.]+),([-\d.]+)\)\s*node\s*"
        r"\{\$([abcde]|\\phi)\$\};")
    for x, y, label in pattern.findall(tex):
        labels[label.replace("\\", "")] = [float(x), float(y)]
    assert set(labels) == {"a", "b", "c", "d", "e", "phi"}
    assert labels == {
        "a": [2.1, .8], "b": [2.9, 3.0], "c": [3.8, 2.7],
        "d": [5.3, 3.0], "e": [5.0, .8], "phi": [4.0, 4.4]}
    return {
        "figure_asset": "morecurves.pdf at scale 0.2",
        "tikz_label_positions": labels,
        "surface_declared_genus": 2,
        "curve_names": list("abcde"),
        "involution_curve_action": {
            "a": "e", "e": "a", "b": "d", "d": "b", "c": "c"},
        "c_fixed_setwise_and_with_orientation": True,
        "fixed_points_declared": 2,
    }


def build_certificate(source_dir):
    source_dir = source_dir.resolve()
    tex_path, figure_path = source_dir / "main.tex", source_dir / "morecurves.pdf"
    assert digest(tex_path) == EXPECTED["main.tex"]
    assert digest(figure_path) == EXPECTED["morecurves.pdf"]
    tex = tex_path.read_text(encoding="utf-8")
    tex_facts = extract_tex_facts(tex)
    with tempfile.TemporaryDirectory(prefix="lp-source-audit-") as temporary:
        directory = Path(temporary)
        svg_path = directory / "morecurves.svg"
        subprocess.run(["pdftocairo", "-svg", str(figure_path), str(svg_path)],
                       check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        vector_facts = classify_vector_paths(svg_path, directory)

    # The figure is inserted at scale .2 into a TikZ picture whose default
    # unit is one centimetre. Bind each TeX label to the corresponding vector
    # layer after converting its placement back to the 1008x612 PDF frame.
    points_per_tikz_unit = 72.27 / 2.54 / .2
    label_binding = {}
    for name in "abcde":
        x, y = tex_facts["tikz_label_positions"][name]
        vector_point = [x * points_per_tikz_unit,
                        612 - y * points_per_tikz_unit]
        distance = point_box_distance(
            vector_point, vector_facts["curve_pixel_bboxes"][name])
        assert distance < 60
        label_binding[name] = {
            "vector_point": [round(value, 3) for value in vector_point],
            "distance_to_named_layer_pixels": round(distance, 3),
        }
    vector_facts["tex_label_binding"] = label_binding

    expected_chain = {"ab": 1, "ac": 0, "ad": 0, "ae": 0,
                      "bc": 1, "bd": 0, "be": 0, "cd": 1,
                      "ce": 0, "de": 1}
    measured = {pair: 1 for pair in vector_facts["surface_intersections"]}
    measured.update(vector_facts["nonconsecutive_overlap_pixels"])
    assert measured == expected_chain
    assert tex_facts["fixed_points_declared"] == \
        vector_facts["fixed_point_dots"]["count"] == 2

    return {
        "format": "luttinger-lp-source-figure-audit-v1",
        "source": {
            "paper": "Lidman--Piccirillo, arXiv:2505.14387v1",
            "retrieval": "https://arxiv.org/e-print/2505.14387v1",
            "file_hashes": EXPECTED,
        },
        "checker_independence": source_audit(),
        "tex_declarations": tex_facts,
        "original_vector_figure": vector_facts,
        "run55_hypotheses": {
            "ordered_five_chain_intersections": expected_chain,
            "involution_reverses_chain_and_preserves_c": True,
            "c_preserved_with_orientation": True,
            "exactly_two_fixed_points": True,
            "source_labels_match": True,
        },
        "result": "PASS: original LP source supplies every Run-55 marked input",
        "remaining_boundary": (
            "standard interpretation of the original handle projection: "
            "dashes denote hidden-side projection rather than extra surface crossings"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True,
                        help="extracted arXiv:2505.14387v1 source directory")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "lp_source_figure_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = build_certificate(args.source_dir)
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output.name} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output.name}")
    print("PASS: immutable LP v1 source hashes match")
    print("PASS: a-b-c-d-e is the ordered five-chain in the original vector figure")
    print("PASS: original prose and vector layer give the chain-reversing involution")
    print("PASS: exactly two fixed points appear both in prose and vector data")
    print(certificate["result"])


if __name__ == "__main__":
    main()
