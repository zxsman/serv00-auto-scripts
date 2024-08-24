const fs = require('fs');
const puppeteer = require('puppeteer');

function formatToISO(date) {
  return date.toISOString().replace('T', ' ').replace('Z', '').replace(/\.\d{3}Z/, '');
}

async function delayTime(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  // 讀取 accounts.json 中的 JSON 字符串
  const accountsJson = fs.readFileSync('accounts.json', 'utf-8');
  const accounts = JSON.parse(accountsJson);

  for (const account of accounts) {
    const { username, password, panelnum } = account;

    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    let url = `https://panel${panelnum}.serv00.com/login/?next=/`;

    try {
      // 修改網址爲新的登錄頁面
      await page.goto(url);

      // 清空用戶名輸入框的原有值
      const usernameInput = await page.$('#id_username');
      if (usernameInput) {
        await usernameInput.click({ clickCount: 3 }); // 選中輸入框的內容
        await usernameInput.press('Backspace'); // 删除原來的值
      }

      // 輸入實際的賬號和密碼
      await page.type('#id_username', username);
      await page.type('#id_password', password);

      // 提交登錄表單
      const loginButton = await page.$('#submit');
      if (loginButton) {
        await loginButton.click();
      } else {
        throw new Error('無法找到登錄按鈕');
      }

      // 等待登錄成功（如果有跳轉頁面的話）
      await page.waitForNavigation();

      // 判斷是否登錄成功
      const isLoggedIn = await page.evaluate(() => {
        const logoutButton = document.querySelector('a[href="/logout/"]');
        return logoutButton !== null;
      });

      if (isLoggedIn) {
        // 獲取當前的UTC時間和北京時間
        const nowUtc = formatToISO(new Date());// UTC時間
        const nowBeijing = formatToISO(new Date(new Date().getTime() + 8 * 60 * 60 * 1000)); // 北京時間東8區，用算術來搞
        console.log(`賬號 ${username} 于北京時間 ${nowBeijing}（UTC時間 ${nowUtc}）登錄成功！`);
      } else {
        console.error(`賬號 ${username} 登錄失敗，請檢查賬號和密碼是否正確。`);
      }
    } catch (error) {
      console.error(`賬號 ${username} 登錄時出現錯誤: ${error}`);
    } finally {
      // 關閉頁面和瀏覽器
      await page.close();
      await browser.close();

      // 用戶之間添加隨機延時
      const delay = Math.floor(Math.random() * 8000) + 1000; // 隨機延時1秒到8秒之間
      await delayTime(delay);
    }
  }

  console.log('所有賬號登錄完成！');
})();

// 自定義延時函數
function delayTime(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
