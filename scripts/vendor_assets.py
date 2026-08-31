"""Copy the locked ECharts distribution after npm ci --ignore-scripts.

Run with --check in CI to verify the shipped bytes against the installed package.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "dist/echarts.min.js": "static/js/echarts.min.js",
    "LICENSE": "static/vendor/echarts-LICENSE",
    "NOTICE": "static/vendor/echarts-NOTICE",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    package = ROOT / "node_modules/echarts"
    expected = json.loads((ROOT / "package.json").read_text())["dependencies"]["echarts"]
    actual = json.loads((package / "package.json").read_text())["version"]
    if actual != expected:
        raise SystemExit("Run npm ci --ignore-scripts before vendoring")
    hashes = {}
    for source, target in FILES.items():
        data = (package / source).read_bytes()
        output = ROOT / target
        hashes[target] = hashlib.sha256(data).hexdigest()
        if args.check:
            if not output.exists() or output.read_bytes() != data:
                raise SystemExit(f"Vendor mismatch: {target}")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
    manifest = json.dumps({"package": "echarts", "version": actual, "sha256": hashes}, indent=2) + "\n"
    target = ROOT / "static/vendor/manifest.json"
    if args.check:
        if target.read_text() != manifest:
            raise SystemExit("Vendor manifest mismatch")
    else:
        target.write_text(manifest)
    print(f"Verified ECharts {actual}" if args.check else f"Vendored ECharts {actual}")


if __name__ == "__main__":
    main()
