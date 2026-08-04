"""
Screaming Frog SEO Spider Integration Client for PythonAiWriter.
Executes headless CLI crawls and interfaces with Screaming Frog local REST API (http://localhost:28018).
"""

import os
import subprocess
import requests
from pathlib import Path
from typing import Dict, Any, Optional


class ScreamingFrogClient:
    """Interface for Screaming Frog CLI execution and local REST API auditing."""

    def __init__(
        self, 
        cli_path: Optional[str] = None, 
        api_url: str = "http://localhost:28018"
    ):
        self.cli_path = cli_path or r"C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe"
        self.api_url = api_url.rstrip("/")

    def is_api_available(self) -> bool:
        """Returns True if Screaming Frog local REST API server is listening."""
        try:
            res = requests.get(f"{self.api_url}/api/v1/system/status", timeout=3)
            return res.ok
        except Exception:
            return False

    def is_cli_available(self) -> bool:
        """Returns True if Screaming Frog CLI executable exists on local machine."""
        return Path(self.cli_path).exists()

    def run_headless_crawl(self, site_url: str, output_folder: Path) -> Tuple[bool, str]:
        """Runs headless CLI crawl in background."""
        if not self.is_cli_available():
            return False, f"Screaming Frog CLI executable not found at '{self.cli_path}'."

        output_folder.mkdir(parents=True, exist_ok=True)
        cmd = [
            self.cli_path,
            "--crawl", site_url,
            "--headless",
            "--export-tabs", "Internal:All,Response Codes:All",
            "--output-folder", str(output_folder)
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if res.returncode == 0:
                return True, f"Crawl finished successfully! Reports saved to:\n{output_folder}"
            else:
                return False, f"CLI Crawl failed (code {res.returncode}): {res.stderr[:200]}"
        except Exception as exc:
            return False, f"CLI Execution Error: {str(exc)}"
