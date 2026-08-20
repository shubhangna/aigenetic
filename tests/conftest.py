"""
Lightweight HTML report generation for the website test suite.

This avoids an extra pytest plugin dependency while still producing an
easy-to-open report after every run.
"""

from __future__ import annotations

from datetime import datetime
from html import escape
import os
from pathlib import Path
import sys
import webbrowser


_HTML_REPORT_RESULTS = []
_HTML_REPORT_STARTED_AT = None


def pytest_addoption(parser):
    parser.addoption(
        "--site",
        action="store",
        default="local",
        choices=("local", "remote"),
        help="Website target: local uses http://localhost:8989, remote uses https://aigenetic.in.",
    )
    parser.addoption(
        "--html-report",
        action="store",
        default="tests/reports/latest.html",
        help="Path for the generated HTML test report.",
    )
    parser.addoption(
        "--no-open-html-report",
        action="store_true",
        default=False,
        help="Generate the HTML report without opening it automatically.",
    )


def pytest_configure(config):
    global _HTML_REPORT_RESULTS, _HTML_REPORT_STARTED_AT
    _HTML_REPORT_RESULTS = []
    _HTML_REPORT_STARTED_AT = datetime.now()

    if "BASE_URL" not in os.environ:
        site_urls = {
            "local": "http://localhost:8989",
            "remote": "https://aigenetic.in",
        }
        os.environ["BASE_URL"] = site_urls[config.getoption("--site")]


def pytest_runtest_logreport(report):
    if report.when not in {"setup", "call", "teardown"}:
        return

    _HTML_REPORT_RESULTS.append(
        {
            "nodeid": report.nodeid,
            "phase": report.when,
            "outcome": report.outcome,
            "duration": report.duration,
            "details": getattr(report, "longreprtext", "") or "",
        }
    )


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    report_path = Path(config.getoption("--html-report")).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    started_at = _HTML_REPORT_STARTED_AT or datetime.now()
    finished_at = datetime.now()
    results = _HTML_REPORT_RESULTS

    totals = {
        "passed": sum(1 for item in results if item["outcome"] == "passed"),
        "failed": sum(1 for item in results if item["outcome"] == "failed"),
        "skipped": sum(1 for item in results if item["outcome"] == "skipped"),
    }

    report_path.write_text(
        _render_report(
            started_at=started_at,
            finished_at=finished_at,
            exitstatus=exitstatus,
            base_url=os.environ.get("BASE_URL", ""),
            totals=totals,
            results=results,
        ),
        encoding="utf-8",
    )

    terminalreporter.write_sep("=", f"HTML report: {report_path}")

    if not config.getoption("--no-open-html-report"):
        _open_report(report_path)


def _open_report(report_path: Path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(report_path)  # type: ignore[attr-defined]
        else:
            webbrowser.open(report_path.as_uri())
    except OSError as exc:
        print(f"Could not open HTML report automatically: {exc}")


def _render_report(started_at, finished_at, exitstatus, base_url, totals, results):
    status = "Passed" if exitstatus == 0 else "Failed"
    duration = (finished_at - started_at).total_seconds()
    rows = "\n".join(_render_result_row(item) for item in results)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Aigenetic Test Report</title>
  <style>
    :root {{
      --bg: #f7f8f6;
      --panel: #ffffff;
      --text: #152023;
      --muted: #687578;
      --border: #dfe4df;
      --pass: #0f7a55;
      --fail: #b42318;
      --skip: #8a5a00;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
    }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 32px 20px 56px;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      gap: 24px;
      align-items: flex-end;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 20px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 30px;
    }}
    .muted {{
      color: var(--muted);
      font-size: 14px;
    }}
    .status {{
      border: 1px solid var(--border);
      background: var(--panel);
      padding: 14px 18px;
      min-width: 130px;
      text-align: center;
      font-weight: 700;
    }}
    .status.passed {{ color: var(--pass); }}
    .status.failed {{ color: var(--fail); }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}
    .metric {{
      background: var(--panel);
      border: 1px solid var(--border);
      padding: 16px;
    }}
    .metric strong {{
      display: block;
      font-size: 26px;
      margin-bottom: 4px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
      border: 1px solid var(--border);
    }}
    th, td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      background: #fbfcfb;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    .pill {{
      display: inline-block;
      min-width: 64px;
      padding: 4px 8px;
      text-align: center;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid currentColor;
    }}
    .passed {{ color: var(--pass); }}
    .failed {{ color: var(--fail); }}
    .skipped {{ color: var(--skip); }}
    details {{
      max-width: 520px;
    }}
    pre {{
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      background: #f6f7f5;
      border: 1px solid var(--border);
      padding: 12px;
      font-size: 12px;
    }}
    @media (max-width: 760px) {{
      header {{ display: block; }}
      .status {{ margin-top: 16px; }}
      .summary {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      table, thead, tbody, th, td, tr {{ display: block; }}
      thead {{ display: none; }}
      tr {{ border-bottom: 1px solid var(--border); }}
      td {{ border-bottom: 0; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>Aigenetic Test Report</h1>
        <div class="muted">Target {escape(base_url)} · Started {escape(started_at.strftime("%Y-%m-%d %H:%M:%S"))} · Finished {escape(finished_at.strftime("%Y-%m-%d %H:%M:%S"))}</div>
      </div>
      <div class="status {escape(status.lower())}">{escape(status)}</div>
    </header>

    <section class="summary">
      <div class="metric"><strong>{totals["passed"]}</strong><span class="muted">Passed phases</span></div>
      <div class="metric"><strong>{totals["failed"]}</strong><span class="muted">Failed phases</span></div>
      <div class="metric"><strong>{totals["skipped"]}</strong><span class="muted">Skipped phases</span></div>
      <div class="metric"><strong>{duration:.2f}s</strong><span class="muted">Duration</span></div>
    </section>

    <table>
      <thead>
        <tr>
          <th>Outcome</th>
          <th>Test</th>
          <th>Phase</th>
          <th>Duration</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  </main>
</body>
</html>
"""


def _render_result_row(item):
    outcome = escape(item["outcome"])
    details = escape(item["details"])
    details_html = (
        f"<details><summary>View failure</summary><pre>{details}</pre></details>"
        if details
        else ""
    )

    return f"""<tr>
  <td><span class="pill {outcome}">{outcome}</span></td>
  <td>{escape(item["nodeid"])}</td>
  <td>{escape(item["phase"])}</td>
  <td>{item["duration"]:.2f}s</td>
  <td>{details_html}</td>
</tr>"""
