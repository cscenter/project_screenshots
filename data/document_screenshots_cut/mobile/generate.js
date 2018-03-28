const puppeteer = require('puppeteer');
const devices   = require('puppeteer/DeviceDescriptors');
const fs        = require('fs')

const screenshot_extension  = ".png";
const output_directory_name = "puppeteer_out";
const mobile_useragent      = "Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A510F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.2704.106 Mobile Safari/537.36"; // uncomment this line to take mobile screenshot
const fixed_resolution      = {"width": 720,"height": 2500}; // comment this line to scroll to the end of the page before taking the screenshot
const border_width          = 15;

const urls_list = fs.readFileSync('../config/urls_list.txt').toString().split('\n')
if (!fs.existsSync(output_directory_name)){
    fs.mkdirSync(output_directory_name);
}

function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
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

      var url_idx = 0;
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
              await page.screenshot({path: file_name + "_fullpage_" + screenshot_extension , fullPage: true});
              const documents = await page.$$("[data-cid]");
              var cnt = 0;
              for (let document of documents) {
                var box = await document.boundingBox();
                if (!box) {
                  console.log("Skipping invisible document...");
                  continue;
                }
                box.x -= border_width;
                box.y -= border_width;
                box.width  += 2 * border_width;
                box.height += 2 * border_width;
                for (i = 0; i < 5; i++) {
                  box.x += Math.floor((Math.random() * 30) - 15);
                  box.y += Math.floor((Math.random() * 150) - 75);
                  box.width += Math.floor((Math.random() * 30) - 15);
                  box.height += Math.floor((Math.random() * 50) - 2);
                  await page.screenshot({path: output_directory_name + "/" + url_idx.toString() + "_" + cnt.toString() + "_" + i + screenshot_extension, clip: box});
                  await timeout(500);
                }
                cnt = cnt + 1;
                console.log("Capturing document at position", await document.boundingBox(), "...");
              }
              // const html = await page.content();
              // fs.writeFile(file_name + ".html", html, (exception) => { if (exception) { throw exception; } });
            } catch (exception) {
              console.log("Exception occured while taking the snapshot of ", url, ":", exception);
            }
            console.log("Saved screenshot and html to", file_name + ".*");
          }
          url_idx += 1;
      }

      console.log("Stopping browser...");
      await browser.close();
    })();
  }, (exception) => {
    console.log("Exception while loading page", exception);
  });
});
