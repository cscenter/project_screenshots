const puppeteer = require('puppeteer');
const devices   = require('puppeteer/DeviceDescriptors');
const fs        = require('fs')

const screenshot_extension  = ".png";
const output_directory_name = "puppeteer_out";
// const mobile_useragent      = "Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A510F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.2704.106 Mobile Safari/537.36"; // uncomment this line to take mobile screenshot
const fixed_resolution      = {"width": 720,"height": 2500}; // comment this line to scroll to the end of the page before taking the screenshot

const urls_list = fs.readFileSync('../config/urls_list.txt').toString().split('\n')
if (!fs.existsSync(output_directory_name)){
    fs.mkdirSync(output_directory_name);
}

puppeteer.launch().then((browser) => {
  console.log("Launching browser...")
  browser.newPage().then((page) => {
    console.log("Loading page...");

    (async () => {
      if (typeof(fixed_resolution) != "undefined") {
        var viewport = page.viewport();
        viewport.width = fixed_resolution.width;
        viewport.height = fixed_resolution.height;
        await page.setViewport(viewport);
        await page.setCacheEnabled(false);
        console.log("Using resolution", fixed_resolution, " on screenshots");
      } else {
        console.log("Using unbounded resolution (may fail on infinitely scrollable pages)");
      }
      if (typeof(mobile_useragent) != "undefined") {
        await page.setUserAgent(mobile_useragent);
        var viewport = page.viewport();
        viewport.isMobile = true;
        viewport.hasTouch = true;
        await page.setViewport(viewport);
        console.log("Running in mobile mode with useragent", mobile_useragent, "...");
      } else {
        console.log("Running in desktop mode...");
      }

      page.setRequestInterception(true);
      page.on('request', request => {
        if (request.resourceType() === 'image')
          request.abort();
        else
          request.continue();
      });

      for (let url of urls_list) {
          if (url) {
            console.log("Creating the snapshot of", url);
            const output_file_prefix = url.replace(/[/:]/g, "_");
            if (output_file_prefix.length > 100) {
              console.log("Filename too long: truncating...");
              output_path = output_file_prefix.substr(1, 100);
            }

            const file_name = output_directory_name + "/" + output_file_prefix;
            try {
              // page.goto docs: https://github.com/GoogleChrome/puppeteer/blob/v1.1.1/docs/api.md#pagegotourl-options
              await page.goto(url, {"waitUntil": "networkidle0"});
              await page.screenshot({path: file_name + screenshot_extension , fullPage: true});
              const html = await page.content();
              fs.writeFile(file_name + ".html", html, (exception) => { if (exception) { throw exception; } });
            } catch (exception) {
              console.log("Exception occured while taking the snapshot of ", url, ":", exception);
            }
            console.log("Saved screenshot and html to", file_name + ".*");
          }
      }

      console.log("Stopping browser...");
      await browser.close();
    })();
  }, (exception) => {
    console.log("Exception while loading page", exception);
  });
});
