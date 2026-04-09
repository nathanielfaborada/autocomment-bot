import asyncio
import os
import random
from pyppeteer import launch
from dotenv import load_dotenv

# Load the settings from the .env file
load_dotenv()


class Watcher:
    """
    One Watcher = one browser window that opens and watches a YouTube video.
    You can create multiple Watchers to watch the same video at the same time.
    """

    def __init__(self, account_id):
        # Give each watcher a number so we know which one is talking in the logs
        self.account_id = account_id

    async def run(self, video_url, watch_duration):
        """
        This is the main job of the watcher:
        1. Open a browser
        2. Go to the YouTube video
        3. Press play
        4. Wait (watch the video)
        5. Close the browser
        """

        # ── Step 1: Open a browser window ──────────────────────────────────
        print(f"[Watcher {self.account_id}] Opening browser...")
        browser = await launch(
            executablePath=os.getenv('CHROME_PATH'),
            headless=False,
            args=[
                '--mute-audio',
                '--disable-blink-features=AutomationControlled',  # hide bot detection
                '--no-first-run',
                '--no-default-browser-check',
            ]
        )

        try:
            page = await browser.newPage()

            # Pretend to be a real Chrome browser so YouTube doesn't block us
            await page.setUserAgent(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            )

            # Hide the "navigator.webdriver" flag that tells YouTube we're a bot
            await page.evaluateOnNewDocument('''() => {
                Object.defineProperty(navigator, "webdriver", { get: () => undefined });
            }''')

            # ── Step 2: Go to the YouTube video ────────────────────────────────
            print(f"[Watcher {self.account_id}] Going to video URL...")
            await page.goto(video_url, timeout=60000, options={'waitUntil': 'load'})

            # If YouTube shows "Something went wrong", refresh once and retry
            if 'Something went wrong' in await page.evaluate('() => document.body.innerText'):
                print(f"[Watcher {self.account_id}] YouTube error detected, refreshing...")
                await asyncio.sleep(3)
                await page.reload(options={'waitUntil': 'load'})
            # 'load' means: wait until the page has fully loaded

            # ── Step 3: Click "Accept all" cookies if YouTube asks ──────────────
            try:
                await page.waitForSelector('button[aria-label="Accept all"]', timeout=5000)
                await page.click('button[aria-label="Accept all"]')
                await asyncio.sleep(1)  # small pause after clicking
            except Exception:
                pass  # no cookies popup? that's fine, just skip

            # ── Step 4: Wait for the video player to appear on the page ─────────
            print(f"[Watcher {self.account_id}] Waiting for video player to load...")
            await page.waitForSelector('video', timeout=15000)
            await asyncio.sleep(2)  # give it a moment to settle

            # ── Step 5: Skip the ad if there is one ─────────────────────────────
            try:
                await page.waitForSelector('.ytp-skip-ad-button', timeout=5000)
                print(f"[Watcher {self.account_id}] Ad found, skipping...")
                await page.click('.ytp-skip-ad-button')
                await asyncio.sleep(1)
            except Exception:
                pass  # no ad? great, skip this step

            # ── Step 6: Force the video to play using JavaScript ─────────────────
            # This talks directly to the video element inside the page
            await page.evaluate('''() => {
                const video = document.querySelector("video");
                if (video) {
                    video.muted = true;  // make sure it's muted
                    video.play();        // press play!
                }
            }''')

            # ── Step 7: Also click the on-screen play button as backup ───────────
            try:
                await page.click('.ytp-play-button')
            except Exception:
                pass  # button not found? JS play above already handled it

            # ── Step 8: Press the K key (YouTube keyboard shortcut for play) ─────
            await page.keyboard.press('k')

            # ── Step 9: Check if the video is actually playing ───────────────────
            is_playing = await page.evaluate('''() => {
                const video = document.querySelector("video");
                return video && !video.paused;  // paused=false means it's playing
            }''')
            print(f"[Watcher {self.account_id}] Is video playing? {is_playing}")

            # ── Step 10: Wait exactly WATCH_DURATION_SECONDS then stop ──────────
            # No matter what happens above, this timer controls when we close.
            print(f"[Watcher {self.account_id}] Watching for {watch_duration} seconds...")
            await asyncio.sleep(watch_duration)

        finally:
            # ── Step 11: ALWAYS close the browser after the timer ───────────────
            # 'finally' means: run this block no matter what —
            # even if there was an error, the browser will still close.
            print(f"[Watcher {self.account_id}] Time's up! Closing browser.")
            try:
                await browser.close()
            except Exception:
                pass  # ignore cleanup errors when browser is already closing


if __name__ == '__main__':

    # Read settings from .env
    video_url      = os.getenv('YOUTUBE_VIDEO_URL')
    watch_duration = int(os.getenv('WATCH_DURATION_SECONDS', 60))
    batch_size     = int(os.getenv('BATCH_SIZE', 5))    # how many browsers open at once
    total_views    = int(os.getenv('TOTAL_VIEWS', 100)) # how many views we want in total

    async def main():
        views_done = 0  # counter: how many views have been completed so far

        while views_done < total_views:

            # Figure out how many to open in this batch
            # (last batch might be less than batch_size, e.g. 3 remaining out of 100)
            remaining   = total_views - views_done
            current_batch_size = min(batch_size, remaining)

            print(f"\n--- Batch starting | Views done: {views_done}/{total_views} | Opening {current_batch_size} browsers ---")

            # Create watchers for this batch only
            watchers = [Watcher(views_done + i + 1) for i in range(current_batch_size)]

            # Run all watchers in this batch at the same time
            tasks = [
                w.run(video_url, watch_duration + random.randint(-10, 10))
                for w in watchers
            ]
            await asyncio.gather(*tasks)
            # By this point all browsers in the batch are closed

            views_done += current_batch_size
            print(f"--- Batch done | Total views completed: {views_done}/{total_views} ---")

            # Small pause between batches so we don't hammer YouTube
            if views_done < total_views:
                pause = random.randint(5, 15)
                print(f"Waiting {pause}s before next batch...")
                await asyncio.sleep(pause)

        print(f"\nDone! {total_views} views completed.")

    asyncio.run(main())
