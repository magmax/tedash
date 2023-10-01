import xml.etree.ElementTree as ET
import json
import datetime

# deprecated
def xml_importer(f):
    tree = ET.parse(f)
    root = tree.getroot()

    result = xml_node_to_dict(root)
    metadata = result["testsuites"]["attr"]
    return metadata, json.dumps(result, indent=2)

# deprecated
def xml_node_to_dict(node):
    data = {}
    if attrib := node.attrib.copy():
        data["attr"] = attrib
    if children := [xml_node_to_dict(x) for x in node]:
        data["children"] = children
    if node.text and (text := node.text.strip()):
        data["text"] = text

    return { node.tag: data }


class JunitImporter:
    def __init__(self, xml):
        self.tree = ET.parse(xml)
        self.root = self.tree.getroot()

        self.data = {
            "metadata": self._import_metadata(self.root),
            "testsuites": self._import_testsuites(),
        }

    @property
    def metadata(self):
        return self.data["metadata"]

    @property
    def json(self, indent=2):
        return json.dumps(self.data, indent=indent)

    def _import_metadata(self, node):
        result = {
            "name": node.attrib["name"],
            "tests": int(node.attrib["tests"]),
            "failures": int(node.attrib["failures"]),
            "errors": int(node.attrib["errors"]),
            "skipped": int(node.attrib["skipped"]),
            "assertions": int(node.attrib["assertions"]),
            "duration": float(node.attrib["time"]),
            "timestamp": node.attrib["timestamp"],
        }
        if "file" in node.attrib:
            result["file"] = node.attrib["file"]
        return result

    def _import_properties(self, node):
        result = {}
        for prop in node:
            result[prop.attrib["name"]] = prop.attrib.get("value", prop.text)
        return result


    def _import_testsuites(self):
        result = []
        for ts in self.root:
            data = {
                    "metadata": self._import_metadata(ts),
                    "properties" : self._import_properties(ts.find("properties")),
                    "testcases": self._import_testcases(ts),
            }
            for prop in ("system-out", "system-err"):
                if (sysout := ts.find(prop)) is not None:
                    data[prop] = sysout.text
            result.append(data)
        return result

    def _import_testcases(self, node):
        result = []
        for tc in node.findall("testcase"):
            data = {
                "name": tc.attrib["name"],
                "classname": tc.attrib["classname"],
                "assertions": int(tc.attrib["assertions"]),
                "duration": float(tc.attrib["time"]),
                "file": tc.attrib["file"],
                "line": int(tc.attrib["line"]),
            }

            for key in ("skipped", "failure", "error"):
                data[key] = False
                if (n := tc.find(key)) is None:
                    continue
                data[key] = True
                if (s := n.attrib.get("message")) is not None:
                    data[f"{key}_message"] = s
                if (s := n.text) is not None:
                    data[f"{key}_description"] = s
                if (s := n.attrib.get("type")) is not None:
                    data[f"{key}_type"] = s
            for key, new in (("system-out", "stdout"), ("system-err", "stderr")):
                if (n := tc.find(key)) is None:
                    continue
                data[new] = n.text
            if (n := tc.find("properties")) is not None:
                data["properties"] = self._import_properties(n)

            result.append(data)
        return result
