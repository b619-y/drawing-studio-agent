"""结构草图的语义/格式回归；不读取私有数据，不替代科学验收。"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
THEME = "20261009-16-SoilAgent-R-Figure1"
SVG = REPO / "output" / "图" / THEME / "20261009-16-系统架构-结构草图.svg"
DRAWIO = REPO / "output" / "脚本" / THEME / "20261009-16-系统架构-关系.drawio"
NS = "{http://www.w3.org/2000/svg}"


class WireframeTests(unittest.TestCase):
    def setUp(self):
        self.root = ET.parse(SVG).getroot()
        self.nodes = {n.get("id"): n for n in self.root.iter() if n.get("id")}
        self.text = " ".join("".join(n.itertext()) for n in self.root.iter(NS + "text"))

    def test_five_unique_modules(self):
        modules = [n.get("id") for n in self.root.iter() if n.get("data-role") == "module"]
        self.assertEqual(modules, ["etl", "csm", "twin", "rtm", "decision"])

    def test_headers_once(self):
        for label in ["0 Auto-ETL", "1 CSM", "2 Digital twin", "3 RTM", "4 Decision"]:
            self.assertEqual(self.text.count(label), 1)

    def test_twin_largest(self):
        widths = {key: int(self.nodes[key].get("data-width")) for key in ["etl", "csm", "twin", "rtm", "decision"]}
        self.assertGreater(widths["twin"], max(v for k, v in widths.items() if k != "twin"))

    def test_editable_vector_only(self):
        forbidden = {"image", "script", "foreignObject", "filter", "linearGradient", "radialGradient"}
        self.assertFalse(any(n.tag.removeprefix(NS) in forbidden for n in self.root.iter()))
        self.assertGreater(len(list(self.root.iter(NS + "text"))), 20)

    def test_unique_ids(self):
        ids = [n.get("id") for n in self.root.iter() if n.get("id")]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_extra_modules_or_claims(self):
        for forbidden in ["Orchestrator", "Scale-up", "knowledge graph", "optimal solution", "autonomous"]:
            self.assertNotIn(forbidden, self.text)

    def test_empty_decision_axes(self):
        axes = self.nodes["decision-axes"]
        self.assertEqual(axes.get("data-state"), "empty-placeholder")
        self.assertFalse(any(n.tag in {NS + "circle", NS + "ellipse", NS + "image"} for n in axes.iter()))
        self.assertIn("No candidate points", self.text)
        for word in ["TIME", "COST", "FLUX", "CONC → color"]:
            self.assertIn(word, self.text)

    def test_conceptual_and_draft_labels(self):
        self.assertIn("Conceptual illustration / not to scale", self.text)
        self.assertIn("STRUCTURE DRAFT", self.text)

    def test_csm_method_guidance(self):
        node = self.nodes["csm-to-twin"]
        self.assertEqual(node.get("data-status"), "method-guidance")
        self.assertIsNotNone(node.get("stroke-dasharray"))

    def test_request_response_directions(self):
        for ident, source, target in [("rtm-to-decision", "rtm", "decision"), ("decision-to-rtm", "decision", "rtm")]:
            self.assertEqual(self.nodes[ident].get("data-source"), source)
            self.assertEqual(self.nodes[ident].get("data-target"), target)

    def test_manual_feedback(self):
        self.assertEqual(self.nodes["user-feedback"].get("data-status"), "manual")
        self.assertIsNotNone(self.nodes["user-feedback"].get("stroke-dasharray"))

    def test_yyc_arial_bold_typography(self):
        canvas = self.nodes["canvas"]
        self.assertEqual(canvas.get("font-family"), "Arial")
        self.assertEqual(canvas.get("font-weight"), "700")
        for node in canvas.iter():
            if node.get("font-family"):
                self.assertEqual(node.get("font-family"), "Arial")
            if node.get("font-weight"):
                self.assertEqual(node.get("font-weight"), "700")

    def test_editable_time_subscripts(self):
        for index in [0, 1]:
            node = self.nodes[f"rtm-time-{index}"]
            self.assertEqual(node.get("data-time-index"), str(index))
            self.assertEqual(node.text, "t")
            subscript = node.find(NS + "tspan")
            self.assertEqual(subscript.text, str(index))
            self.assertGreater(float(subscript.get("dy")), 0)

    def test_no_external_refs(self):
        for node in self.root.iter():
            for key, value in node.attrib.items():
                if key.rsplit("}", 1)[-1] == "href":
                    self.assertTrue(value.startswith("#"))

    def test_drawio_reserved_ids_and_connections(self):
        nodes = list(ET.parse(DRAWIO).getroot().iter("mxCell"))
        ids = {n.get("id") for n in nodes}
        self.assertTrue({"0", "1"}.issubset(ids))
        self.assertEqual(len(ids), len(nodes))
        edges = {(n.get("source"), n.get("target")) for n in nodes if n.get("edge") == "1"}
        self.assertTrue({("etl", "csm"), ("csm", "twin"), ("twin", "rtm"), ("rtm", "decision"), ("decision", "rtm")}.issubset(edges))
        for node in nodes:
            if node.get("edge") == "1":
                self.assertIn(node.get("source"), ids)
                self.assertIn(node.get("target"), ids)
                self.assertEqual(node.find("mxGeometry").get("relative"), "1")


if __name__ == "__main__":
    unittest.main()
