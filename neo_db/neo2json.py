"""Generate the browser snapshot directly from the local canonical relationship file."""
import json

from graph_data import ROOT, chart_data, relations


def main():
    output = ROOT / "static/data.json"
    output.write_text(json.dumps(chart_data(relations()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
