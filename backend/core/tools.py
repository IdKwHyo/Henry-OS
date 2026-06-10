from playwright.async_api import async_playwright

class Tools:
    async def browser_search(self, query: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(f"https://duckduckgo.com/?q={query}")
                # Extract snippet (simplified)
                snippet = await page.inner_text(".result__snippet")
                return f"Web result: {snippet[:500]}"
            except Exception as e:
                return f"Browser error: {e}"
            finally:
                await browser.close()