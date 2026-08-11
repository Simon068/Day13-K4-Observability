"""Capture trace metadata screenshots scrolled deep enough to show prompt_label fields."""
import time
from pathlib import Path

EVIDENCE_DIR = Path("submission/evidence")
PROJECT = "cmsod2r0900m6ad0hzg8w1vot"
BASE = f"https://us.cloud.langfuse.com/project/{PROJECT}"

PAGES = [
    ("trace_baseline_metadata.png", f"{BASE}/traces/8dc7c893d2a418600e7e9f9904047d00"),
    ("trace_candidate_metadata.png", f"{BASE}/traces/65e356bfe5fc5ca71c7799ed27dc7be7"),
    ("challenge_waterfall.png", f"{BASE}/traces/c709ac1e15ee347068438f5464d7bb13"),
]


def main():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        
        for filename, url in PAGES:
            print(f"\nCapturing {filename}")
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception:
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                except Exception:
                    pass
            
            time.sleep(5)
            
            # Switch to JSON view which shows all metadata inline
            try:
                json_toggle = page.locator("button:has-text('JSON'), label:has-text('JSON')").first
                if json_toggle.is_visible():
                    json_toggle.click()
                    time.sleep(2)
                    print("  Switched to JSON view")
            except Exception as e:
                print(f"  Could not switch to JSON: {e}")
            
            # Scroll down to where prompt_label should be visible
            # The metadata section is at the bottom of the panel
            page.evaluate("window.scrollTo(0, 1500)")
            time.sleep(2)
            
            # Check if prompt_label is visible
            try:
                visible = page.locator("text=prompt_label").is_visible()
                print(f"  prompt_label visible: {visible}")
                if not visible:
                    # Try scrolling within the right panel content
                    page.evaluate("""
                        const panels = document.querySelectorAll('[class*=scroll], [style*=overflow]');
                        panels.forEach(p => p.scrollTop = p.scrollHeight);
                    """)
                    time.sleep(2)
                    visible = page.locator("text=prompt_label").is_visible()
                    print(f"  prompt_label visible after inner scroll: {visible}")
            except Exception:
                pass
            
            filepath = EVIDENCE_DIR / filename
            page.screenshot(path=str(filepath), full_page=False)
            print(f"  Saved: {filepath} ({filepath.stat().st_size} bytes)")
        
        page.close()
        browser.close()
    
    print("\nDone!")


if __name__ == "__main__":
    main()
