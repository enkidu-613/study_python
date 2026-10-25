# 08 · HTML、CSS 与 JavaScript：浏览器里的文档和交互

> David J. Malan / CS50 团队，Harvard University
>
> 非官方中文改编，依据 Harvard CS50x 当前课程资料编写；原课程资料许可为 CC BY-NC-SA 4.0。本文件不是 Harvard 官方翻译或课程材料。使用与改编说明见[本目录来源与许可](来源与许可.md)。

前一章用 SQL 查询关系数据。现在把同一批知识文档放到浏览器里：HTML 描述内容，CSS 决定呈现，JavaScript 响应用户动作。下一章再由 Flask 接手服务器端请求。

## 本章学什么

- 看懂一次浏览器请求如何经过 URL、DNS、IP、路由器、TCP/UDP、HTTP/HTTPS 到达服务器。
- 用一个完整本地 HTML 文件建立语义结构、样式与交互，不依赖 Node、框架或外部 API。
- 能追踪 `input` 事件从浏览器产生、经过监听器到更新页面的完整调用链。
- 知道前端过滤只是展示层功能，不能替代服务器授权或数据库查询。

本章不做完整前端工程、打包器、第三方框架、复杂异步请求、身份认证或生产部署。官方讲义还展示正则表达式和 CSS 框架；本章用浏览器本地格式检查和机制说明覆盖这两项，但不引入框架依赖。

## 前置与运行方式

前置：能读简单 Python/SQL、理解变量和函数。HTML/CSS/JavaScript 都是本章新内容；Python 已学过，但不是网页的运行语言。

完整示例只需浏览器。将下面唯一的 `web-notes.html` 保存到 `examples/cs50x/` 后，双击打开即可。也可在仓库根目录执行：

```bash
open examples/cs50x/web-notes.html
```

这是 macOS 的打开文件命令；Windows 可用 `start examples/cs50x/web-notes.html`，Linux 桌面可用 `xdg-open examples/cs50x/web-notes.html`。这些只是打开本地文件，不会启动服务。预期看到目录表格；本地打开后还应检查布局与浏览器 Console。

## 先看完整程序

文件：`examples/cs50x/web-notes.html`。这是完整单文件，包含 HTML、CSS 和 JavaScript；复制时不要只取脚本部分。

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>知识文档目录</title>
  <style>
    :root { font-family: system-ui, sans-serif; color: #17212b; background: #f4f7f8; }
    body { max-width: 52rem; margin: 0 auto; padding: 1.5rem; }
    header, main, footer { padding: 1rem 0; }
    h1 { margin-bottom: .25rem; }
    .muted { color: #52616b; }
    label { display: block; margin: 1rem 0 .35rem; font-weight: 700; }
    input { box-sizing: border-box; width: 100%; padding: .7rem; font: inherit; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; background: white; }
    th, td { border-bottom: 1px solid #d5dfe3; padding: .65rem; text-align: left; }
    th { background: #e5eff1; }
    .status { min-height: 1.5em; }
    .format-check { margin: 1.5rem 0; padding: 1rem 0; border-block: 1px solid #d5dfe3; }
    @media (max-width: 32rem) {
      body { padding: .75rem; }
      th, td { padding: .45rem .25rem; }
    }
  </style>
</head>
<body>
  <header>
    <h1>知识文档目录</h1>
    <p class="muted">本地演示：按标题或负责人筛选三条示例记录。</p>
  </header>

  <main>
    <label for="filter">筛选文档</label>
    <input id="filter" type="search" autocomplete="off"
           placeholder="例如 Python、HTTP 或 9">
    <p id="status" class="status" aria-live="polite"></p>

    <section class="format-check" aria-labelledby="format-heading">
      <h2 id="format-heading">本地格式检查</h2>
      <label for="email">课程邮箱示例（要求以 .edu 结尾）</label>
      <input id="email" name="email" type="email" required
             pattern=".+@.+\.edu" placeholder="student@example.edu">
      <button id="check-email" type="button">检查格式</button>
      <p id="email-status" aria-live="polite"></p>
    </section>

    <table>
      <caption>文档与负责人的对应关系</caption>
      <thead>
        <tr><th scope="col">ID</th><th scope="col">标题</th><th scope="col">负责人</th></tr>
      </thead>
      <tbody id="documents">
        <tr><td>1</td><td>Python 入门</td><td>7</td></tr>
        <tr><td>2</td><td>HTTP 请求</td><td>7</td></tr>
        <tr><td>3</td><td>SQL 查询</td><td>9</td></tr>
      </tbody>
    </table>
    <p id="empty" hidden>没有匹配的文档。</p>
  </main>

  <footer class="muted">示例数据只在当前 HTML 文件中，不会写入真实应用或数据库。</footer>

  <script>
    const filterInput = document.querySelector("#filter");
    const rows = Array.from(document.querySelectorAll("#documents tr"));
    const status = document.querySelector("#status");
    const emptyMessage = document.querySelector("#empty");
    const emailInput = document.querySelector("#email");
    const emailStatus = document.querySelector("#email-status");
    const checkEmailButton = document.querySelector("#check-email");

    function filterDocuments() {
      const query = filterInput.value.trim().toLocaleLowerCase();
      let visibleCount = 0;

      for (const row of rows) {
        const searchableText = row.textContent.toLocaleLowerCase();
        const matches = searchableText.includes(query);
        row.hidden = !matches;
        if (matches) visibleCount += 1;
      }

      emptyMessage.hidden = visibleCount !== 0;
      status.textContent = `显示 ${visibleCount} / ${rows.length} 条`;
    }

    filterInput.addEventListener("input", filterDocuments);
    filterDocuments();

    checkEmailButton.addEventListener("click", function () {
      if (emailInput.checkValidity()) {
        emailStatus.textContent = "符合本地格式规则；没有发送到服务器。";
      } else {
        emailInput.reportValidity();
        emailStatus.textContent = "格式不符合本地规则。";
      }
    });
  </script>
</body>
</html>
```

预期页面初始显示三条记录和“显示 3 / 3 条”。输入 `python` 后只剩 Python 入门；输入 `9` 后只剩负责人为 9 的 SQL 查询；输入 `xyz` 时出现“没有匹配的文档”，状态显示 `显示 0 / 3 条`。清空输入恢复三条。

格式检查中输入 `student@example.edu` 再点按钮，页面显示“符合本地格式规则；没有发送到服务器。”；输入 `student@example.com` 时，浏览器报告格式不匹配。没有任何邮箱被提交或保存。

## 先追踪运行顺序

1. 浏览器读取 HTML 字节，解析标签，建立一棵文档对象模型（Document Object Model，DOM，浏览器对 HTML 元素形成的可操作对象树）。`document.querySelector` 从这棵树查找元素。
2. 浏览器解析 `<style>`，把选择器匹配到元素并计算最终样式；窄屏时 `@media` 规则覆盖部分布局。
3. 浏览器读到脚本，`filterInput` 指向 `<input>` 对应的 DOM 元素；`rows` 是三个 `<tr>` 元素组成的数组。
4. `addEventListener("input", filterDocuments)` 把监听器登记在输入框上。这里不是输入框“自动运行了 JS”：浏览器检测到用户输入后创建 `input` 事件，再调用已登记的 `filterDocuments` 函数。
5. 函数读取当前 `filterInput.value`，对每行文本做不区分大小写的包含判断，再改 DOM 的 `hidden` 属性与状态文字。
6. 最后的 `filterDocuments()` 是我们主动直接调用一次，所以不用先打字也有正确初始状态。

| 变量 | 创建时刻 | 保存什么 | 谁在何时读取/改变 |
| --- | --- | --- | --- |
| `filterInput` | 脚本执行时 | 一个输入框 DOM 引用 | 每次输入事件中读取 `.value` |
| `rows` | 脚本执行时 | 三个表格行的数组 | `filterDocuments` 遍历；页面本身不增删行 |
| `query` | 每次调用函数 | 本次标准化后的搜索文字 | 本轮每一行匹配时读取 |
| `visibleCount` | 每次调用函数 | 本轮命中的行数 | 命中一行就增加 1，最后显示 |

注意 `rows` 是页面结构的快照。如果后续代码动态添加新行，旧数组不会自动长出新行，需要重新查询或自行维护集合。本例故意不加动态增删，避免把核心事件机制藏进额外状态管理。

## 一次请求怎样找到服务器

网络不是“浏览器直接连上一个名字”。以访问 `https://example.com/docs?q=python` 为例：

- URL（Uniform Resource Locator，统一资源定位符）是资源地址。这里协议是 `https`，主机是 `example.com`，路径是 `/docs`，查询字符串是 `q=python`。
- DNS（Domain Name System，域名系统）把主机名解析成一个或多个 IP 地址。DNS 不是网页内容库；它回答“这个名字该联系哪个地址”。浏览器、操作系统、递归 DNS 服务器可能缓存结果，所以并非每次都从根服务器重新查询。
- DHCP（Dynamic Host Configuration Protocol，动态主机配置协议）通常让本地网络中的设备自动取得 IP 配置，例如本机地址、网关和 DNS 服务器。它不是 DNS，也不负责给网站域名分配目的地址。
- IP（Internet Protocol，网际协议）给数据包标注源和目的 IP 地址，并让路由器逐跳转发。路由器只需根据路由信息选择下一跳；路径可能改变，也不承诺应用数据完整有序。
- TCP（Transmission Control Protocol，传输控制协议）在传统 HTTPS over TCP 中提供有序、可靠的字节流与重传。端口把同一台主机上的不同服务区分开，例如 HTTPS 常用 443。UDP（User Datagram Protocol，用户数据报协议）提供更轻量的数据报，不保证交付或顺序；DNS 常用 UDP，但也会用 TCP，现代 HTTP/3 则运行于 QUIC/UDP。因此“网页一定用 TCP”不准确。
- HTTP（Hypertext Transfer Protocol，超文本传输协议）规定请求与响应的结构。浏览器请求中带方法、路径、标头与可能的正文；服务器返回状态码、标头与内容。
- HTTPS 是 HTTP 通过 TLS（传输层安全协议）保护连接。TLS 让客户端验证服务器证书，并加密传输、校验传输完整性；它不保证网站内容诚实、不自动修复服务器授权漏洞，也不等于“提交内容就安全”。

简化路径：用户输入 URL → 浏览器确定主机/端口 → DNS 查询地址（若缓存未命中）→ IP 数据包经路由器转发 → TCP 或 QUIC 建立传输 → TLS（HTTPS）协商保护 → HTTP 请求/响应。DHCP 更早在设备接入网络时提供本地配置，不是每个网页请求中的一跳。

IP 地址标识网络端点；域名便于人阅读；端口标识主机上的服务。它们不能互相替代。一个域名可能有多个地址，一个 IP 也可能承载多个域名网站。

## HTTP 请求与状态

HTTP 方法描述客户端希望服务器做什么。GET 通常用于读取资源，数据常放在 URL 查询参数中；POST 通常提交请求正文以创建或处理数据。它们的安全属性不由方法名称保证：POST 不会自动加密，是否加密取决于 HTTPS；GET URL 可能进入历史记录、服务器日志、分享链接。

状态码是服务器对一次请求的结果分类：`200` 成功、`302` 重定向、`400` 请求格式/输入问题、`404` 路径不存在、`500` 服务器内部错误。浏览器开发者工具的 Network 面板能看到方法、URL、状态、标头和响应体；它是定位 HTTP 问题的观察窗口。

GET 应当设计成读取，不应因为访问页面就悄悄删除或购买。浏览器、代理和爬虫可能重复请求或预取 GET 页面。POST 也可能被重复提交，服务器仍需考虑幂等性、重复订单和 CSRF；这些在 Flask 章再落到代码。

## HTML：有语义的文档

HTML（HyperText Markup Language，超文本标记语言）描述页面有哪些内容及其关系。标签写成 `<p>文字</p>`；元素通常由开始标签、内容和结束标签构成。属性写在开始标签中，例如 `<html lang="zh-CN">` 的 `lang` 指明文档语言。

`<!doctype html>` 声明 HTML5 文档；`<html>` 是根；`<head>` 放标题、字符集、视口等元数据；`<body>` 放页面可见内容。`<title>` 的文字出现在浏览器标签页，不等同于页面内的 `<h1>`。

优先选择能表达内容角色的语义元素：`<header>`、`<nav>`、`<main>`、`<section>`、`<footer>`；标题按层次用 `<h1>` 到 `<h6>`；段落用 `<p>`；链接用 `<a href="...">`；无序/有序列表用 `<ul>/<ol>` 与 `<li>`；表格只用于有行列关系的数据，使用 `<caption>`、`<th scope="col">` 和 `<td>`。

表单用 `<form>` 包含输入与提交按钮。`<label for="filter">` 的 `for` 必须匹配控件 `id="filter"`，这样点击标签也能聚焦输入框，并让辅助技术知道标签对应哪个控件。输入类型如 `type="email"` 可提供浏览器级格式提示，但客户端验证可以被绕开，服务器仍必须重新校验。

无障碍（Accessibility，尽量让不同能力和输入方式的人都可使用）不是给页面贴个标签就结束：有意义的标题结构、可键盘操作的原生控件、文字标签、足够的对比度、表格标题、动态状态提示能让读屏与键盘用户理解页面。本例用 `aria-live="polite"` 提示过滤结果；`aria-*` 不能取代语义 HTML。

## CSS：样式如何竞争

CSS（Cascading Style Sheets，层叠样式表）规定元素如何呈现。CSS 规则形如 `选择器 { 属性: 值; }`。本例 `#filter` 对应 `id="filter"`；`.muted` 对应 `class="muted"`；`table` 是元素选择器。

- `id` 在一个文档中应唯一，常用于精确定位一个元素；`class` 可重复，用于一组具有共同用途的元素。
- 选择器有优先级（specificity，特异性）：大致上内联样式高于 ID，高于 class/属性/伪类，高于元素选择器；同层级且同特异性时，后出现的规则通常胜出。`!important` 会打乱正常层叠，应克制使用。
- 继承指某些属性（如字体、文字颜色）从父元素传给子元素；边框、外边距等通常不继承。继承不是所有 CSS 属性的通用默认。
- 盒模型（box model，盒子模型）包含内容区、内边距 `padding`、边框 `border` 和外边距 `margin`。`box-sizing: border-box` 让设置的宽度包含 padding 和 border，便于控制总尺寸。
- 本例用 `max-width` 限制长行，用 `margin: 0 auto` 水平居中，用 `width: 100%` 适应窄屏，并用 `@media` 在小视口调整间距。响应式布局是根据可用视口调整排布，不是只把桌面网页缩小。

正则表达式（regular expression，描述文本模式的一种小语言）用于匹配字符串形状。页面中的 `pattern=".+@.+\.edu"` 表示：`.+` 是至少一个任意字符，`@` 是字面 at 符号，反斜线加句点 `\.` 匹配字面句点，最后要求 `edu`；浏览器对整个输入值做模式检查，`type="email"` 另外检查基本邮箱格式。它只是格式提示，不验证邮箱真实存在、不验证用户身份，更不能授权访问；用户可绕开浏览器直接请求服务器，所以服务器必须独立验证业务规则。

CSS 框架（framework）是预先写好的 CSS（有些还包含 JavaScript 组件）及其命名/布局约定。以 Bootstrap 为例，页面先在 `<head>` 载入其 stylesheet，浏览器下载后按框架定义的 class 规则呈现 `.container`、`.btn` 等类；这些 class 不是 HTML 内置功能，也不会在未加载 stylesheet 时自动生效。框架能减少重复造样式，但带来版本、下载、约定和可访问性检查成本。本例用自己的几条 CSS 规则就够了，所以不需要网络依赖。

## JavaScript：事件驱动的 DOM 更新

JavaScript 是浏览器可执行的编程语言，用于条件、循环、函数和交互。DOM API 是浏览器提供的对象接口，并非 JavaScript 语言本身。

`const filterInput = document.querySelector("#filter")` 调用浏览器 DOM 方法，返回第一个匹配元素或 `null`。`const` 表示变量绑定不能重新赋值，不代表引用的 DOM 内容永远不变。`function filterDocuments() { ... }` 定义一个函数；只有调用它才执行函数体。

`addEventListener` 是 DOM 元素上的方法，接收事件名与回调函数（callback，稍后由另一个执行方调用的函数）。浏览器因用户输入而触发 `input` 事件时，调用我们的回调。`input` 在键盘输入、粘贴、清除等输入值变化时触发；它比只看 `keyup` 更贴近“值改变”本身。监听器注册时不要写 `filterDocuments()`，否则会立刻调用并把返回值 `undefined` 交给监听器；要传函数本身 `filterDocuments`。

`textContent` 读写纯文本，适合显示用户输入；`innerHTML` 会把字符串按 HTML 解析，若拼进不可信文字会造成跨站脚本（XSS）。本例读 `row.textContent` 做过滤、写 `status.textContent` 写结果，没有把输入拼成 HTML。若要高亮匹配词，应创建 DOM 节点并设置 `textContent`，不要把原始查询串拼进 `innerHTML`。

完整调用链不是一句“绑定事件”：脚本执行 → 浏览器取得 input 元素 → 监听器记录函数引用 → 用户输入使浏览器产生 input 事件 → 浏览器调用函数 → 函数读当前值 → 逐行计算 → 改变每行 `hidden` → 浏览器重绘。

## 改动并验证

1. 输入 `HTTP`，预测命中数量后再观察。大小写转换后，标题 `HTTP 请求` 应命中。
2. 把表格中 SQL 的负责人从 `9` 改为 `7`，刷新后输入 `9` 应从一条变成零条；输入 `7` 应显示三条。这证明过滤针对页面现有文本，而不是数据库。
3. 将 `filterInput.addEventListener("input", filterDocuments);` 暂时注释，刷新后打字：状态不变。这验证浏览器事件到处理函数的调用关系。恢复后再操作。
4. 将状态更新中的 `textContent` 改成 `innerHTML` 并输入 `<b>demo</b>`。本例状态仅输出固定数字而没有回显查询，所以不会触发注入；不要据此得出 `innerHTML` 安全。试着把查询拼进 `innerHTML` 是危险示范，禁止在真实网页运行。
5. 用浏览器开发者工具检查元素：input 的 `id` 与 label 的 `for` 是否相同，表格行是否按输入得到 `hidden` 属性，Console 是否有错误。

本地 HTML 的输入只筛选硬编码的三行。它没有网络请求，不连贯穿项目中的数据库，也没有授权能力。即使前端把别人记录隐藏，用户仍可能修改页面或直接发请求；真正的数据访问控制要在服务器验证，下一章会用 Flask 与 SQLite 展示。

## 常见坑

- `querySelector` 找不到元素时会返回 `null`；拼错 `id` 后再访问 `.value` 会报错。浏览器 Console 可检查。
- `<label for>` 与控件 `id` 不对应时，标签点击和读屏关联失败。
- CSS 的 `#x` 是 ID 选择器，`.x` 是 class 选择器；HTML 中 `id="x"` 和 `class="x"` 也不同。
- `addEventListener("input", filterDocuments())` 在注册时立即执行函数，不是传回调。
- `innerHTML` 不是普通文本输出；用 `textContent` 能避免把输入解释成 HTML。
- `display: none` 和 `hidden` 会让内容不显示；筛选结果文本仍需要说明数量与空结果。
- GET 查询参数会出现在 URL；不要把密码或秘密放入 URL。HTTP 与 HTTPS 的差别也不由 GET/POST 决定。
- 浏览器输入校验只改善体验，不构成服务器安全校验。
- `pattern` 检查文本格式，不检查账号是否归用户所有，也不是授权机制。

## 独立练习：按 ID 筛选

需求：仍用同一份文档目录，把搜索框改为只接受文档 ID；`1`、`2`、`3` 分别显示一行，空字符串显示三行，`8` 显示零行与空结果提示。

约束：单一 HTML 文件、原生 HTML/CSS/JavaScript，不加库，不访问真实应用/数据库，不用 `innerHTML`。

验收：说明哪个 DOM 属性保存用户输入；写出由谁调用处理函数的时序；手工验证 `2`、空字符串、`8` 三个输入；键盘可聚焦，label 能聚焦输入框，空结果有可读提示。

## 对应官方资料与作业

本章正文依据 [CS50x Week 8](https://cs50.harvard.edu/x/weeks/8/) 与 [Lecture 8 notes](https://cs50.harvard.edu/x/notes/8/) 的 Internet、Routers、DNS、DHCP、HTTPS、HTML、Regular Expressions、CSS、Frameworks、JavaScript 主题。网络路由/IP/TCP/UDP、URL/HTTP、HTML 语义、CSS 规则与 JS DOM 事件在正文或完整示例中逐项落地；HTML `pattern` 是本地可验证实验，CSS 框架则解释其载入和 class 生效机制。

官方问题集入口是 [Problem Set 8](https://cs50.harvard.edu/x/psets/8/)，其中 [Homepage](https://cs50.harvard.edu/x/psets/8/homepage/) 要求用 HTML、CSS、JavaScript 做个人主页。中文主题说明：为一个兴趣主题安排清晰语义内容、可读样式与真实交互，并亲自检查不同屏幕与输入；官方要求和提交规范以原页面为准。这里不提供官方题解。

## 课后压缩

心智模型：HTML 是内容树，CSS 是呈现规则，JavaScript 读取事件并更新 DOM；请求则经过名称解析、寻址、传输和 HTTP 协议抵达服务器。

最小交互模板：取得 DOM 元素 → `addEventListener("input", handler)` → handler 读 `.value` → 用 `textContent` 或属性更新结果。

边界：前端过滤不等于数据库查询；浏览器校验不等于服务器验证。复习问题：浏览器何时调用 `filterDocuments`，以及为什么把查询拼进 `innerHTML` 是另一类风险？

## 导航

- 上一章：[07 · SQL 与关系数据库](07_SQL与关系数据库.md)
- 下一章：[09 · Flask 与 Web 应用](09_Flask与Web应用.md)
- 本目录：[CS50x 中文课程索引](README.md)
