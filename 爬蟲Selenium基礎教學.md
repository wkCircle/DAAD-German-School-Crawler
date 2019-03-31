#Tutorial Source: [github.com/wkCircle](<https://github.com/wkCircle/DAAD-German-School-Crawler>)

# 爬蟲Selenium基礎教學

**先備條件**: selenium和環境

- 安裝beautifulsoup package

- 安裝parse: html5lib, lxml etc.

- ```bash
  $ pip3 install selenium.
  $ pip3 install BeautifulSoup4
  $ pip3 install lxml
  $ pip3 install html5lib
  ```

- 下載安裝webdriver: [selenium official website](<https://www.seleniumhq.org/download/>)
- 將下載好的webdriver丟到你的python所在路徑(\\...\\python3.6\\)
- **安裝[Katalon Recorder](<https://chrome.google.com/webstore/detail/katalon-recorder/ljdobmomdgdljniojadhoplhkpialdid?hl=zh-TW>) (以下教學以Chrome為例子，搭配Katalon Recorder Extension可快速把介面滑鼠操作轉為程式碼。(亦可下載官方的Selenium IDE取代Katalon))**

**以DAAD查詢德國學校Program為例子**

- 先觀察我們要爬的[網頁](<https://www.daad.de/deutschland/studienangebote/studiengang/en/?a=result&q=°ree=37&subjects%5B380%5D=1&studyareas%5B380%5D=1&studyfields%5B394%5D=1&studyfields%5B390%5D=1&courselanguage=2&locations=&universities%5B1%5D=1&admissionsemester=&sort=name&page=1>)樣子
- 觀察網址變動情況
- 點進去每一個program，看細部內容，我們的目標是把program所有欄位資訊抓下來存成表格。

*有想法了嗎？*

流程是:















**給個爬網頁起始點 &rarr; loop over 頁碼 &rarr; 在每個網頁底下，爬完所有program(有0-10個) &rarr; &diams; 每個program都要爬3個tab 底下的欄位資訊 &rarr; 分析擷取重要資訊 &rarr; 暫存到變數裡 &rarr; 爬完一定數量寫入檔案(遊戲記錄點概念) &rarr; 清空暫存變數 &rarr; 回到 &diams; 重複動作。**

來看Code!!

難爬的例子: [看這裡](<https://booth.e-taitra.com.tw/zh-TW/m/2019FD/5>)(本章教學完畢)















# 如何啟用你的電腦GPU

**先備條件**

- 檢查你的電腦(裝置管理員)，需要有Nvidia的顯示卡。
- 更新你的顯卡驅動程式至最新(版本>385.54)，可透過裝置管理員的自動更新驅動程式選項/或者到[nVIDIA官網](https://www.nvidia.com.tw/Download/index.aspx?lang=tw)依據你的顯示卡規格下載最新驅動程式。
- 安裝[VS2017](https://visualstudio.microsoft.com/downloads/)或更新的版本，需事先加入Community(需與你系統相容)，點選C++的桌面開發。

**安裝驅動程式與測試**

1. [CUDA](https://goo.gl/We59k2)，請務必選擇Local下載方式，因Network安裝根據經驗易有缺漏。安裝過程請選自定，僅勾選CUDA即可。

2. [cnDNN](https://goo.gl/JS6BKr)，一樣需事先加入社群，然後根據你剛剛安裝的CUDA版本來挑選要安裝的版本。
   下載後將檔案解壓縮至 C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0中

3. 測試: 進入Terminal 輸入指令 

   ```bash
   $ nvcc -V
   ```

   檢查是否安裝成功。

**安裝PyTorch**

Go to [here](<https://pytorch.org/get-started/locally/>) and select the corresponding setting according to your computer environment. Below will generate codes for you to install pytorch. E.g., see the following figure.(本章教學完畢)

![pytorch installation box](http://www.programmersought.com/images/283/404fa6fd89b6945e67fa5293b0b3a823.png)