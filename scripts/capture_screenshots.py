"""Capture Langfuse screenshots by connecting to existing Edge via CDP."""
import time
from pathlib import Path

EVIDENCE_DIR = Path("submission/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

PROJECT = "cmsod2r0900m6ad0hzg8w1vot"
BASE = f"https://us.cloud.langfuse.com/project/{PROJECT}"

PAGES = [
    ("trace_list.png", f"{BASE}/traces", "Trace list >= 10"),
    ("trace_baseline_metadata.png", f"{BASE}/traces/8dc7c893d2a418600e7e9f9904047d00", "Baseline V1 metadata"),
    ("trace_candidate_metadata.png", f"{BASE}/traces/65e356bfe5fc5ca71c7799ed27dc7be7", "Candidate V2 metadata"),
    ("prompt_versions.png", f"{BASE}/prompts/day13-chat", "Prompt V1 + V2 with labels"),
    ("challenge_waterfall.png", f"{BASE}/traces/c709ac1e15ee347068438f5464d7bb13", "Challenge rag_slow waterfall"),
]


def main():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        # Connect to Edge already running with --remote-debugging-port=9222
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # Use existing context (which has the user's login session)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        
        for filename, url, desc in PAGES:
            print(f"\nCapturing {filename}: {desc}")
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception:
                print(f"  Timeout on networkidle, using domcontentloaded...")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                except Exception:
                    pass
            
            time.sleep(5)
            
            # For trace detail pages, scroll down to show metadata
            if "traces/" in url and not url.endswith("/traces"):
                try:
                    page.evaluate("window.scrollTo(0, 400)")
                    time.sleep(2)
                except Exception:
                    pass
            
            filepath = EVIDENCE_DIR / filename
            page.screenshot(path=str(filepath), full_page=False)
            size = filepath.stat().st_size
            print(f"  Saved: {filepath} ({size} bytes)")
            
            if size < 20000:
                print(f"  WARNING: File seems too small, might be an error page!")
        
        page.close()
        browser.close()
    
    print("\nDone!")


if __name__ == "__main__":
    main()
