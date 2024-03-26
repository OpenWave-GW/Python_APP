# Python_APP
<a href="http://www.youtube.com/watch?v=BNPRGuqg0ew
" target="_blank"><img src="/image/YT_screenshot.jpg" 
alt="IMAGE ALT TEXT HERE" width="400" height="220" border="10" /></a>

## MPO-2000介紹
MPO系列是固緯電子第一款可在機器上直接執行Python腳本的示波器。在Python腳本的控制下，MPO可控制外部USB設備進行協同測試，可用來 __實現小型自動化與半自動化測試系統__ 。

<img src="/image/automation_test_system2.png" alt="Image Description" width="500" height="360">

MPO-2000集多種量測儀器於一身，特別適合教學應用。在Python腳本的控制下能做到多種以往示波器單機無法實現的功能，例如 __BJT I-V 特性曲線繪製__ (需要配合使用 __GDP-025__ 以轉換出電流值)。

<img src="/image/automation_test_system1.png" alt="Image Description" width="500" height="360">

<img src="/image/bjt01.png" alt="Image Description" width="400" height="300">

<img src="/image/bjt_I_V_curve.png" alt="Image Description" width="400" height="240">

我們將撰寫MPO Python腳本時所需要的各種 __Python模組__ (如垂直檔位、水平檔位、觸發模式、任意波產生器、數位萬用表、可程式直流電源供應器等常用控制函式)整理在這裡，方便使用者參考，使用者可依需求進行修改。

MPO-2000上 __內建多種Python APP__ ，其源碼可在選單功能中直接複製出來。使用者可依需要自行修改以符合不同的測試需求。

這裡也提供了一些MPO機器上沒有的Python範例腳本供使用者參考。

### 在Python腳本的控制下MPO-2000可控制外部設備

MPO-2000在Python腳本的控制下，可透過USB介面以 __USB CDC-ACM__ 協議控制外接USB設備，進行多機協作測試。

可連接的設備包括 __PSW__、__PFR__、__PPX__、__PEL__ 和 __GDM__ 等系列。(MPO也可透過 __LAN__ 以 __socket__ 協議控制外部設備)

這項特點使得MPO適用於小型自動化與半自動化測試的應用，利用Python腳本自動執行量測任務，可以為工程師節省非常多時間與人力。

### MPO-2000非常適合用在學校教學與工業量測應用
MPO-2000的多合一功能結合Python腳本，可以實現多種不同的應用。例如:
   * 電晶體I-V特性曲線
   * LED I-V特性曲線
   * MQTT Publisher可實現量測數據上傳雲端
   * MQTT Subscriber可實現地球另一端的遠端控制
   * 結合社群軟體的事件通知 - 如WeChat 
   * 元件耐受性測試
   * 實驗數據自動採集
   * 電路的頻率與溫度特性曲線量測
   * 結合條碼掃描器的量測應用

### 其他特點
MPO-2000還具備下面的功能特點，包含:
   * 可同時顯示兩個通道的頻譜分析，並可同時顯示其 __瀑布圖__ 。
   * 除了 __UART__ 、 __I2C__ 、 __SPI__ 、 __CAN__ 和 __LIN__ 的串列信號解碼功能，還提供了 __CAN-FD__ 、 __USB 2.0 Full Speed__ 、 __FlexRay__ 、 __I2S__ 和 __USB Power Delivery__ 等通訊協議的解碼功能
   * MPO-2000還提供了 __Web Server__ 與 __Web Control__ 功能，可在同一區域網路內使用PC或手機上的Browser觀察動態波形與遠端操控。

## 功能限制
如果您需要在MPO-2000上撰寫Python腳本 __控制外部USB設備__ ，或是調用 __Python繪圖庫__ 設計選單或圖表，您必須選購Professional版的MPO-2000P示波器。Professional版還具備將.py檔打包為Python APP安裝檔的功能。

Basic版機器雖然具備有限的Python能力，但所安裝的Python APP若有使用繪圖庫與控制外部USB設備的功能，仍然是可以執行的。

## 相關資訊
有關產品的進一步資訊，可以到GW Instek網站[MPO產品頁面](https://www.gwinstek.com/en-global/products/detail/MPO-2000)取得。

如果你想進一步了解有關MPO上的Python程式設計，可以先看下面這份文件 => [MPO-2000 Python Tutorial and Application Handbook](https://www.gwinstek.com/en-global/products/detail/MPO-2000) (在下載頁面)

```MPO-2000B的使用者可選購升級選配(MP2-PRO)，使其具備MPO-2000P的全部功能```
