import nest_asyncio

nest_asyncio.apply()

import asyncio
from playwright.async_api import Playwright, async_playwright


pause_to_record = False
# pause_to_record = True

slow_mo = 50
moz_creds = "assets/mozcreds.txt"
chrome_exe = "/usr/bin/google-chrome"
downloads_path = "/home/ubuntu/Downloads"
user_data = "/home/ubuntu/.config/google-chrome/"
# user_data = "session"


def in_notebook():
    """Return True if run from a Jupyter Notebook and False if not."""
    try:
        import IPython

        if IPython.get_ipython().__class__.__name__ == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        else:
            return False  # Other type (likely a script)
    except NameError:
        return False  # Probably standard Python interpreter


if in_notebook():
    keyword = "Foo"  # or set to any default value that you prefer
    headless = False
else:
    import argparse

    headless = True
    parser = argparse.ArgumentParser(description="Example script")
    parser.add_argument(
        "-k", "--keyword", type=str, required=True, help="Value for keyword"
    )
    args = parser.parse_args()
    keyword = args.keyword

with open(moz_creds) as fh:
    UN, PW = [x.strip().split(" ")[1] for x in fh.readlines()]


async def main():
    async with async_playwright() as playwright:
        context = await playwright.chromium.launch_persistent_context(
            viewport={"width": 1200, "height": 800},
            downloads_path=downloads_path,
            executable_path=chrome_exe,
            user_data_dir=user_data,
            accept_downloads=True,
            headless=headless,
            channel="chrome",
            slow_mo=slow_mo,
        )
        page = await context.new_page()
        await page.goto("https://moz.com/")

        # Codegen activated
        if pause_to_record:
            await page.pause()  # Edit this line in for codegen and out for automation.

        # -- BEGIN CODEGEN LINES --
        try:
            await page.get_by_role("link", name="Log in").click()
            await page.locator("#email").click()
            await page.locator("#email").fill(UN)
            await page.locator("#email").press("Tab")
            await page.locator("#password").fill(PW)
            await page.locator("#password").press("Enter")
            await page.get_by_role("navigation").get_by_role(
                "link", name="Moz Pro"
            ).click()
        except:
            ...

        await page.goto(
            "https://analytics.moz.com/pro/keyword-explorer/keyword/suggestions?locale=en-US"
        )
        await page.get_by_placeholder(
            "Enter a term or phrase to get analysis, suggestions, difficulty, and more"
        ).fill(keyword)
        await page.get_by_role("button", name="analyze").click()
        async with page.expect_download() as download_info:
            await page.get_by_role("button", name="Export CSV").click()
        download = download_info.value
        download = await download
        await download.save_as("downloads/" + download.suggested_filename)
        # -- END CODEGEN LINES --

        # When done, close the browser.
        await asyncio.sleep(2)
        await context.close()


async def run_main():
    await main()


if in_notebook():
    try:
        asyncio.get_running_loop()
        asyncio.run(run_main())
    except RuntimeError as e:
        if "no running event loop" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_main())
else:
    asyncio.run(run_main())
