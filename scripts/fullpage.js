const puppeteer = require('puppeteer');
const devices   = require('puppeteer/DeviceDescriptors');
const fs        = require('fs')

const screenshot_extension = ".png";
// you may find the list of availible mobile devices here: https://github.com/GoogleChrome/puppeteer/blob/master/DeviceDescriptors.js
// const mobile_device        = devices["Nexus 7"]; // uncomment this line to take a mobile screenshot
const fixed_resolution     = {"width": 1280,"height": 2000} // uncomment this line to scroll to the end of the page before taking the screenshot

const urls_list = fs.readFileSync('config/urls_list.txt').toString().split('\n')

puppeteer.launch().then((browser) => {
  console.log("Launching browser...")
  browser.newPage().then((page) => {
    console.log("Loading page...");

    (async () => {
      if (typeof(fixed_resolution) != "undefined") {
        await page.setViewport(fixed_resolution);
        console.log("Using resolution", fixed_resolution, " on screenshots");
      } else {
        console.log("Using unbounded resolution (may fail on infinitely scrollable pages)");
      }
      if (typeof(mobile_device) != "undefined") {
        await page.emulate(mobile_device);
        console.log("Running in mobile mode...");
      } else {
        console.log("Running in desktop mode...");
      }

      for (let url of urls_list) {
          if (url) {
            console.log("Creating the snapshot of", url);
            const output_path = url.replace(/[/:]/g, "_");

            try {
              // page.goto docs: https://github.com/GoogleChrome/puppeteer/blob/v1.1.1/docs/api.md#pagegotourl-options
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

      console.log("Stopping browser...");
      await browser.close();
    })();
  }, (exception) => {
    console.log("Exception while loading page", exception);
  });
})
