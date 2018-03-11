const puppeteer = require('puppeteer');

const screenshot_extension = ".png";

puppeteer.launch().then((browser) => {
  console.log("Launching browser...")
  browser.newPage().then((page) => {
    console.log("Loading page...");

    (async () => {
      await page.setViewport({"width": 1280,"height": 720});

      const fs = require('fs')
      for (let url of fs.readFileSync('config/urls_list.txt').toString().split('\n'))
      {
          if (url) {
            console.log("Creating the snapshot of", url);
            const output_path = url.replace(/[/:]/g, "_");

            try {
              await page.goto(url, {"waitUntil": "networkidle0"})
              await page.screenshot({path: output_path + screenshot_extension , fullPage: true})
              const html = await page.content();
              fs.writeFile(output_path + ".html", html, (exception) => { if (exception) { throw exception; } });
            } catch (exception) {
              console.log("Exception occured while taking the snapshot of ", url, ":", exception);
            }
            console.log("Saved screenshot and html to", output_path + ".*");
          }
      }

      await browser.close();
      console.log("Stopping browser...");
    })();
  }, (exception) => {
    console.log("Exception while loading page", exception);
  });
})
