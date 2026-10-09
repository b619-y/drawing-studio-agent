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
        for label in ["0 Auto-ETL", "1 CSM", "2 Digital twin", "3 RTM", "4 MOPSO"]:
            self.assertEqual(self.text.count(label), 1)

    def test_model_only_titles(self):
        for module, label in [("etl", "0 Auto-ETL"), ("csm", "1 CSM"), ("twin", "2 Digital twin"), ("rtm", "3 RTM"), ("decision", "4 MOPSO")]:
            title = self.nodes[f"{module}-method-label"]
            self.assertIn(title, list(self.nodes[module]))
            self.assertEqual(title.get("data-role"), "module-title")
            self.assertEqual(title.text, label)
            self.assertEqual(title.get("y"), "200")
        self.assertFalse(any(n.get("data-role") in {"process-title", "method-label"} for n in self.root.iter()))
        for old_title in ["Conceptualization", "Site reconstruction", "Reaction prediction", "Plan optimization"]:
            self.assertNotIn(old_title, self.text)

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
        self.assertIn("Decision axes contain no candidate data", self.root.find(NS + "desc").text)
        axis_text = " ".join("".join(n.itertext()) for n in axes.iter(NS + "text"))
        for word in ["CONC", "COST", "FLUX"]:
            self.assertIn(word, axis_text)
        self.assertNotIn("TIME", axis_text)
        conc = self.nodes["decision-axis-conc"]
        self.assertEqual((conc.get("x"), conc.get("y")), ("1685", "493"))
        self.assertIn("TIME remains a fourth optimization objective", self.root.find(NS + "desc").text)

    def test_clean_figure_notes_in_metadata(self):
        for removed in ["Color: CONC", "STRUCTURE DRAFT", "Dashed:", "Conceptual illustration / not to scale"]:
            self.assertNotIn(removed, self.text)
        desc = self.root.find(NS + "desc").text
        for retained in ["Structure draft pending review", "conceptual illustration", "not to scale", "not a measured field", "methodological guidance"]:
            self.assertIn(retained, desc)

    def test_shared_resources_footer_removed(self):
        self.assertNotIn("shared-resources", self.nodes)
        self.assertNotIn("Shared data / tools", self.text)
        self.assertFalse(any(n.get("data-role") == "resources" for n in self.root.iter()))
        self.assertFalse(any(n.get("d") == "M60 755 L1740 755" for n in self.root.iter(NS + "path")))

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

    def test_right_side_text_hierarchy(self):
        balance = self.nodes["rtm-balance-equation"]
        partition = self.nodes["rtm-partition-equation"]
        output = self.nodes["model-response-label"]
        request = self.nodes["candidate-request-label"]
        scheme = self.nodes["candidate-schemes-label"]
        self.assertEqual(balance.get("data-equals-x"), partition.get("data-equals-x"))
        self.assertLess(float(balance.get("data-baseline")), float(partition.get("data-baseline")))
        self.assertLess(float(output.get("y")), float(request.get("y")))
        self.assertLess(float(request.get("y")), float(scheme.get("y")))
        self.assertLess(float(request.get("y")), float(balance.get("data-baseline")))
        self.assertEqual(self.nodes["decision-method-label"].get("x"), scheme.get("x"))
        self.assertEqual(output.text, "Outputs")
        self.assertEqual(request.text, "Plans")

    def test_eight_twin_fields_and_rtm_equations(self):
        fields = self.nodes["twin-parameter-fields"].get("data-fields").split(",")
        self.assertEqual(fields, ["K", "Kd", "alpha", "lambda", "lambda_active", "R", "v", "D"])
        self.assertEqual(len(set(fields)), 8)
        self.assertEqual(self.nodes["rtm-balance-equation"].get("data-equation"), "dM/dt = −∑F − r")
        self.assertEqual(self.nodes["rtm-partition-equation"].get("data-equation"), "Cs = Kd Cw")
        self.assertEqual(["".join(n.itertext()) for n in self.nodes["rtm-partition-equation"].iter(NS + "text")], ["Cs", "=", "Kd Cw"])
        for removed in ["Geometry / initial fields / support", "Time evolution", "Mass checks"]:
            self.assertNotIn(removed, self.text)

    def test_compact_aligned_annotation_rows(self):
        self.assertEqual(self.root.get("viewBox"), "0 0 1800 630")
        self.assertEqual(self.root.get("height"), "63mm")
        for ident in ["etl-annotations", "csm-annotations", "twin-parameter-fields", "rtm-equations", "decision-output"]:
            group = self.nodes[ident]
            self.assertEqual(group.get("data-final-baseline"), "590")
            self.assertEqual(list(group.iter(NS + "text"))[-1].get("y"), "590")
        for ident in ["etl-annotations", "csm-annotations", "twin-parameter-fields"]:
            self.assertEqual([n.get("y") for n in self.nodes[ident].iter(NS + "text")], ["550", "590"])

    def test_rtm_native_fraction_and_aligned_equals(self):
        self.assertEqual(self.nodes["rtm-balance-numerator"].text, "dM")
        self.assertEqual(self.nodes["rtm-balance-denominator"].text, "dt")
        self.assertEqual(self.nodes["rtm-balance-numerator"].get("x"), self.nodes["rtm-balance-denominator"].get("x"))
        self.assertEqual(self.nodes["rtm-fraction-rule"].tag, NS + "path")
        self.assertEqual(self.nodes["rtm-balance-equals"].get("x"), self.nodes["rtm-partition-equals"].get("x"))
        self.assertEqual(self.nodes["rtm-balance-rhs"].get("x"), self.nodes["rtm-partition-rhs"].get("x"))

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
