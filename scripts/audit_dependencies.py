"""Audit every registry package/version in uv.lock, including optional platforms.

Install the dev group first. A vulnerability, skipped package, unsupported source,
or failed lookup fails this check. No advisory IDs are suppressed.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def locked_requirements():
    lock = tomllib.loads((ROOT / "uv.lock").read_text())
    requirements = set()
    for package in lock["package"]:
        source = package["source"]
        if source == {"virtual": "."}:
            continue
        if source != {"registry": "https://pypi.org/simple"}:
            raise ValueError(f"Cannot audit non-PyPI source: {package['name']}")
        requirements.add(f"{package['name']}=={package['version']}")
    if not requirements:
        raise ValueError("The lockfile has no auditable packages")
    return sorted(requirements)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Save pip-audit JSON evidence")
    args = parser.parse_args()
    requirements = locked_requirements()
    with tempfile.TemporaryDirectory(prefix="kgqa-audit-") as directory:
        source = Path(directory) / "requirements.txt"
        report = Path(directory) / "report.json"
        source.write_text("\n".join(requirements) + "\n")
        result = subprocess.run([
            sys.executable, "-m", "pip_audit", "-r", str(source),
            "--no-deps", "--disable-pip", "--progress-spinner", "off",
            "--format", "json", "--output", str(report),
        ], check=False)
        if not report.is_file():
            raise SystemExit(result.returncode or 1)
        data = json.loads(report.read_text())
        if args.output:
            args.output.write_text(report.read_text())
        packages = data["dependencies"]
        scanned = {f"{package['name']}=={package.get('version')}" for package in packages}
        if result.returncode or scanned != set(requirements) or any(
            package.get("skip_reason") or package.get("vulns") for package in packages
        ):
            raise SystemExit("Dependency audit failed; inspect the report and scanner output")
        print(f"Audited all {len(packages)} locked packages: zero known vulnerabilities, zero skipped")


if __name__ == "__main__":
    main()
