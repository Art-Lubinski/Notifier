  const puppeteer = require('puppeteer');

 let scrape = async () => {
     const browser = await puppeteer.launch({headless: false});
     const page = await browser.newPage();
     await page.goto('https://sso.verizonenterprise.com/amserver/sso/login.go');

     await page.waitFor('input[name=userId]');
     await page.$eval('input[name=userId]', el => el.value = 'WORLDINC4G');
     await page.waitFor('input[name=password]');
     await page.$eval('input[name=password]', el => el.value = 'W663300w');
     await page.click('button[type="submit"]');
     await page.waitFor(10000);
     await page.goto('https://b2b.verizonwireless.com/sms/amsecure/unbilledusage/unbilledUsage.go');
     await page.waitFor(10000);
     await page.select('#selectedMtnNumber', '929-236-5003')
     await page.waitFor(10000);
     const info = await page.evaluate(() => {
        var IDs = new Object();
          IDs['total_usage'] = $("#usedDataSpanData").text();
          IDs['allowed'] = $("#totalDataSpanData").text();
          IDs['days'] = $("#daysRemaining").text();
          IDs['line_usage'] = $("#lineDataUsgGB").text();
        return IDs;
        });
      await page.goto('https://b2b.verizonwireless.com/sms/amsecure/unbilledusage/allLinesUsage.go?mtn=929-236-5003');  
        const teams = await page.evaluate(()=>{
          const grabFromRow = (row, classname) => row
          .querySelector(`td.${classname}`)
          .innerText
          .trim()

         const TEAM_ROW_SELECTOR = 'tr.data-row'
         const data = []
         const teamRows = document.querySelectorAll(TEAM_ROW_SELECTOR)
         for(const tr of teamRows){
           data.push({
             name: grabFromRow(tr, 'mtn'),
             usage: grabFromRow(tr, 'usage')
           })
         }
         return data
        })

      await page.close();
     await browser.close();

    var data = new String(info.total_usage + " " + info.allowed + " " + info.days);


    const fs = require('fs');
    fs.writeFile("C:\\Program Files\\Notifier\\Data\\verizon_usage.txt", data, function(err) {
    if(err) {
        return console.log(err);
    }
})
fs.writeFile("C:\\Program Files\\Notifier_v2\\Data\\verizon_lines_usage.json", JSON.stringify(teams,null,2), function(err) {
if(err) {
    return console.log(err);
}
})

};


 scrape()
