# 安全修复记录 · 2026-08-31

修复基准为原始提交 7c3966a。此记录对应本地工作区改动，**没有推送、关闭或 dismiss GitHub 告警**。下表是已完成的本地措施；线上是否关闭，必须等更新进入默认分支并由 GitHub 重新扫描后确认。

## 验证结果

| 检查 | 修复前 | 修复后 |
| --- | --- | --- |
| GitHub Dependabot 页面 | 62 条 open，逐页读取全部告警 | 本地逐条处理 62/62；线上状态待发布后核验 |
| Python pip-audit | 79 条漏洞记录、16 个受影响包；另有 py2neo 4.1.0 无法在 PyPI 查验 | uv.lock 全部 42 个第三方包：0 条已知漏洞、0 个跳过 |
| npm audit | 无 npm 锁文件，旧 jQuery 是直接提交的脚本 | ECharts、zrender、tslib：0 条已知漏洞 |
| 运行环境 | 旧 requirements 混入开发、Jupyter、爬虫依赖 | Python 3.14.7；最小运行环境只有 7 个包 |
| 回归检查 | 本次最初 6 个安全回归用例全部失败 | 31 项 pytest 通过，Ruff 通过 |
| 实际静态文件 | jQuery 2.2.4、旧 ECharts、Bootstrap/Nifty | 仅 ECharts 6.1.0 及应用原生 JS；vendor 校验通过 |
| 浏览器 | 全图 JSON 无法解析，搜索/问答不可用 | 全图、搜索、画像、两层多分支问答和无结果提示已实测 |

Python 与 GitHub 的数字口径不同：独立扫描器按其数据库报告依赖版本的漏洞记录，不应把 79 当成 GitHub 新增的告警数。“零已知漏洞”不代表不存在未知漏洞或业务逻辑风险。扫描结果是本次检查时的快照。

## 遗留资源清理补充

按后续清理要求删除 README 的迁移、来源与许可章节，以及 203 个无关或不再使用的文件（5,719,749 字节），包括红楼梦的 180 张画像、105 份简介、188 条关系、旧爬虫/notebook、字体、背景图和流程图。

三国 122 份简介迁至 data/profiles.json，122 张画像统一迁至 data/portraits/，逐文件 SHA-256 与原文件一致；146 条规范关系及供核对的三国原始关系表保留。爬虫和 notebook 的依赖组移除，锁定第三方包由 77 个减至 42 个。31 项回归测试、Ruff、vendor 校验通过，新扫描为零已知漏洞、零跳过。历史审计证据和仍使用的 ECharts LICENSE/NOTICE 保留，不改写项目的历史来源。

## 原始告警按包汇总

| 依赖 | 告警数 | 本地处理 | 原告警编号 |
| --- | ---: | --- | --- |
| certifi | 2 | 升级并锁定为 2026.7.22 | #20, #39 |
| flask | 2 | 升级并锁定为 3.1.3 | #27, #69 |
| flask-caching | 1 | 移除；不再声明、安装或加载 | #10 |
| ipython | 2 | 移除；历史 notebook/爬虫已删除，不再安装 | #12, #53 |
| jinja2 | 6 | 升级并锁定为 3.1.6 | #2, #5, #47, #48, #58, #59 |
| jquery | 1 | 移除；不再声明、安装或加载 | #40 |
| jupyter-core | 1 | 移除；历史 notebook/爬虫已删除，不再安装 | #18 |
| numpy | 5 | 移除；历史 notebook/爬虫已删除，不再安装 | #13, #14, #16, #34, #80 |
| py | 1 | 移除；不再声明、安装或加载 | #7 |
| pygments | 4 | 升级并锁定为 2.21.0 | #6, #8, #36, #73 |
| pytest | 1 | 升级并锁定为 9.1.1 | #75 |
| tornado | 16 | 移除；历史 notebook/爬虫已删除，不再安装 | #28, #38, #50, #51, #56, #61, #70, #71, #74, #76, #77, #78, #79, #81, #82, #83 |
| urllib3 | 11 | 升级并锁定为 2.7.0 | #1, #3, #11, #35, #41, #42, #45, #52, #63, #65, #66 |
| werkzeug | 9 | 升级并锁定为 3.1.8 | #4, #21, #23, #24, #49, #54, #64, #67, #68 |

应用不再使用 py、Flask-Caching 或 jQuery；不是用忽略规则掩盖它们。后续按清理要求删除了旧 notebook 和爬虫，NumPy、IPython、Tornado 等依赖随之完全移出锁文件；其余依赖仍纳入全锁文件审计。运行 requirements 从锁文件重新导出，原过期清单已替换。

## 额外修复

- ECharts 更新至 6.1.0，修复其旧版 XSS 风险。依据：[GHSA-fgmj-fm8m-jvvx](https://github.com/advisories/GHSA-fgmj-fm8m-jvvx)。
- Bootstrap 3.4.1 仍有已知 XSS；因此移除 Bootstrap/jQuery/Nifty 及不再使用的页面样式，使用原生 JS/CSS。依据：[GHSA-q58r-hwc8-rm9j](https://github.com/advisories/GHSA-q58r-hwc8-rm9j)、[GHSA-vxmc-5x29-h64v](https://github.com/advisories/GHSA-vxmc-5x29-h64v)。
- 运行路径移除停止维护的 py2neo 和无法直接用于 Python 3.14 的旧 pyltp。Neo4j 仅作可选导入，使用官方驱动和环境变量密码。
- 默认不连接数据库；导入不再清空数据库，用参数化 MERGE 写入专用标签，数据不拼接为 Cypher。
- 关闭 Flask 调试器并只监听本机；限制请求体和输入长度。人物画像校验白名单，拒绝路径穿越；简介按纯文本显示，图表 tooltip 使用 richText。
- 添加 CSP、nosniff、禁止嵌入和 referrer 策略。style-src 仍允许 inline 样式，以兼容图表；script-src 不允许 inline 脚本或 eval。
- 修复损坏的静态 JSON，使用本地去重关系和三国简介；问答保留全部成功路径，不把无匹配包装成确定的历史结论。
- 引入 Python pin、uv 锁文件、前端资源清单、只读权限的 CI 和 Dependabot。GitHub Actions 固定到已核对的提交 SHA。

## 复现与证据

完整命令见 [README 开发与安全检查](../../README.md#开发与安全检查)。Python 审计入口：

    uv run --locked python scripts/audit_dependencies.py

可加 --output /path/to/report.json 保存新证据，不要覆盖本次基准。脚本提取 uv.lock 全部 PyPI 包及版本，不按当前操作系统过滤，不忽略任何 advisory。依赖缺失、来源不支持、查询失败或跳过都导致失败。

本地验证环境为 macOS、Python 3.14.7、uv 0.12.7。新建最小环境没有 Neo4j、NumPy、pyltp 或 pytest，仍能加载页面并返回两层问答。真实浏览器验证了 1280px 桌面、390px 手机宽度，无横向页面溢出。浏览器回归是人工驱动的验收，不是 CI 自动端到端测试。

- [GitHub 62 条告警](dependabot-baseline-2026-08-31.json)
- [逐条处理映射 JSON](dependabot-remediation-2026-08-31.json)
- [Python 修复前扫描](pip-audit-before.json)
- [第一阶段修复后扫描：77 包](pip-audit-after.json)
- [遗留资源清理后全锁文件扫描：42 包](pip-audit-after-cleanup.json)
- [npm 修复后扫描](npm-audit-after.json)
- [桌面多分支问答](qa-desktop.png)
- [手机人物搜索](search-mobile.png)

## 仍需明确的边界

1. 本地改动尚未推送或合并，不能把线上 62 个 open 标记为已关闭。更新默认分支后需核对原告警及新增告警；不要通过 dismiss 消除计数。
2. 已编写 GitHub Actions，尚未在远程 runner 执行；本地通过不能代替远程首次运行。
3. 未连接真实 Neo4j；旧爬虫和历史 notebook 已删除，不作为受支持功能。单元测试验证参数化导入及不含删除语句，不是数据库并发或兼容性集成测试。
4. 项目是本地教学工具，不承诺公网生产安全。历史图谱的阵营、关系和简介仍待史料校订；本次未替历史采集材料作新的许可认定。
5. profile/QA 的 JSON 返回结构有变化，有限语法替代旧 NLP 入口；旧客户端需按当前 app.py 的路由返回结构适配。

## 每条原告警的本地处理

所有行的线上状态均为“等待发布后重扫”。

| 原告警 | 依赖 | 标题 | 本地处理 |
| --- | --- | --- | --- |
| [#1](https://github.com/BrambleXu/KGQA_SG/security/dependabot/1) | urllib3 | Exposure of Sensitive Information to an Unauthorized Actor in urllib3 | 升级并锁定为 2.7.0 |
| [#2](https://github.com/BrambleXu/KGQA_SG/security/dependabot/2) | jinja2 | Jinja2 sandbox escape via string formatting | 升级并锁定为 3.1.6 |
| [#3](https://github.com/BrambleXu/KGQA_SG/security/dependabot/3) | urllib3 | Improper Certificate Validation in urllib3 | 升级并锁定为 2.7.0 |
| [#4](https://github.com/BrambleXu/KGQA_SG/security/dependabot/4) | werkzeug | Pallets Werkzeug Insufficient Entropy | 升级并锁定为 3.1.8 |
| [#5](https://github.com/BrambleXu/KGQA_SG/security/dependabot/5) | jinja2 | Regular Expression Denial of Service (ReDoS) in Jinja2 | 升级并锁定为 3.1.6 |
| [#6](https://github.com/BrambleXu/KGQA_SG/security/dependabot/6) | pygments | Pygments vulnerable to Regular Expression Denial of Service (ReDoS) | 升级并锁定为 2.21.0 |
| [#7](https://github.com/BrambleXu/KGQA_SG/security/dependabot/7) | py | py vulnerable to Regular Expression Denial of Service | 移除；不再声明、安装或加载 |
| [#8](https://github.com/BrambleXu/KGQA_SG/security/dependabot/8) | pygments | Infinite Loop in Pygments | 升级并锁定为 2.21.0 |
| [#10](https://github.com/BrambleXu/KGQA_SG/security/dependabot/10) | flask-caching | Deserialization of Untrusted Data in Flask-Caching | 移除；不再声明、安装或加载 |
| [#11](https://github.com/BrambleXu/KGQA_SG/security/dependabot/11) | urllib3 | CRLF injection in urllib3 | 升级并锁定为 2.7.0 |
| [#12](https://github.com/BrambleXu/KGQA_SG/security/dependabot/12) | ipython | Execution with Unnecessary Privileges in ipython | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#13](https://github.com/BrambleXu/KGQA_SG/security/dependabot/13) | numpy | Buffer Copy without Checking Size of Input in NumPy | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#14](https://github.com/BrambleXu/KGQA_SG/security/dependabot/14) | numpy | NumPy NULL Pointer Dereference | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#16](https://github.com/BrambleXu/KGQA_SG/security/dependabot/16) | numpy | Incorrect Comparison in NumPy | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#18](https://github.com/BrambleXu/KGQA_SG/security/dependabot/18) | jupyter-core | Execution with Unnecessary Privileges in JupyterApp | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#20](https://github.com/BrambleXu/KGQA_SG/security/dependabot/20) | certifi | Certifi removing TrustCor root certificate | 升级并锁定为 2026.7.22 |
| [#21](https://github.com/BrambleXu/KGQA_SG/security/dependabot/21) | werkzeug | Pallets Werkzeug vulnerable to Path Traversal | 升级并锁定为 3.1.8 |
| [#23](https://github.com/BrambleXu/KGQA_SG/security/dependabot/23) | werkzeug | Incorrect parsing of nameless cookies leads to __Host- cookies bypass | 升级并锁定为 3.1.8 |
| [#24](https://github.com/BrambleXu/KGQA_SG/security/dependabot/24) | werkzeug | High resource usage when parsing multipart form data with many fields | 升级并锁定为 3.1.8 |
| [#27](https://github.com/BrambleXu/KGQA_SG/security/dependabot/27) | flask | Flask vulnerable to possible disclosure of permanent session cookie due to missing Vary: Cookie header | 升级并锁定为 3.1.3 |
| [#28](https://github.com/BrambleXu/KGQA_SG/security/dependabot/28) | tornado | Open redirect in Tornado | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#34](https://github.com/BrambleXu/KGQA_SG/security/dependabot/34) | numpy | NumPy Buffer Overflow (Disputed) | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#35](https://github.com/BrambleXu/KGQA_SG/security/dependabot/35) | urllib3 | Improper Neutralization of CRLF Sequences in urllib3 library for Python | 升级并锁定为 2.7.0 |
| [#36](https://github.com/BrambleXu/KGQA_SG/security/dependabot/36) | pygments | Pygments vulnerable to ReDoS | 升级并锁定为 2.21.0 |
| [#38](https://github.com/BrambleXu/KGQA_SG/security/dependabot/38) | tornado | Tornado vulnerable to HTTP request smuggling via improper parsing of `Content-Length` fields and chunk lengths | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#39](https://github.com/BrambleXu/KGQA_SG/security/dependabot/39) | certifi | Removal of e-Tugra root certificate | 升级并锁定为 2026.7.22 |
| [#40](https://github.com/BrambleXu/KGQA_SG/security/dependabot/40) | jquery | XSS in jQuery as used in Drupal, Backdrop CMS, and other products | 移除；不再声明、安装或加载 |
| [#41](https://github.com/BrambleXu/KGQA_SG/security/dependabot/41) | urllib3 | `Cookie` HTTP header isn't stripped on cross-origin redirects | 升级并锁定为 2.7.0 |
| [#42](https://github.com/BrambleXu/KGQA_SG/security/dependabot/42) | urllib3 | Authorization Header forwarded on redirect | 升级并锁定为 2.7.0 |
| [#45](https://github.com/BrambleXu/KGQA_SG/security/dependabot/45) | urllib3 | urllib3's request body not stripped after redirect from 303 status changes request method to GET | 升级并锁定为 2.7.0 |
| [#47](https://github.com/BrambleXu/KGQA_SG/security/dependabot/47) | jinja2 | Jinja vulnerable to HTML attribute injection when passing user input as keys to xmlattr filter | 升级并锁定为 3.1.6 |
| [#48](https://github.com/BrambleXu/KGQA_SG/security/dependabot/48) | jinja2 | Jinja vulnerable to HTML attribute injection when passing user input as keys to xmlattr filter | 升级并锁定为 3.1.6 |
| [#49](https://github.com/BrambleXu/KGQA_SG/security/dependabot/49) | werkzeug | Werkzeug debugger vulnerable to remote execution when interacting with attacker controlled domain | 升级并锁定为 3.1.8 |
| [#50](https://github.com/BrambleXu/KGQA_SG/security/dependabot/50) | tornado | Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') in tornado | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#51](https://github.com/BrambleXu/KGQA_SG/security/dependabot/51) | tornado | Tornado has a CRLF injection in CurlAsyncHTTPClient headers | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#52](https://github.com/BrambleXu/KGQA_SG/security/dependabot/52) | urllib3 | urllib3's Proxy-Authorization request header isn't stripped during cross-origin redirects | 升级并锁定为 2.7.0 |
| [#53](https://github.com/BrambleXu/KGQA_SG/security/dependabot/53) | ipython | IPython vulnerable to command injection via set_term_title | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#54](https://github.com/BrambleXu/KGQA_SG/security/dependabot/54) | werkzeug | Werkzeug safe_join not safe on Windows | 升级并锁定为 3.1.8 |
| [#56](https://github.com/BrambleXu/KGQA_SG/security/dependabot/56) | tornado | Tornado has an HTTP cookie parsing DoS vulnerability | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#58](https://github.com/BrambleXu/KGQA_SG/security/dependabot/58) | jinja2 | Jinja has a sandbox breakout through indirect reference to format method | 升级并锁定为 3.1.6 |
| [#59](https://github.com/BrambleXu/KGQA_SG/security/dependabot/59) | jinja2 | Jinja2 vulnerable to sandbox breakout through attr filter selecting format method | 升级并锁定为 3.1.6 |
| [#61](https://github.com/BrambleXu/KGQA_SG/security/dependabot/61) | tornado | Tornado vulnerable to excessive logging caused by malformed multipart form data | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#63](https://github.com/BrambleXu/KGQA_SG/security/dependabot/63) | urllib3 | urllib3 redirects are not disabled when retries are disabled on PoolManager instantiation | 升级并锁定为 2.7.0 |
| [#64](https://github.com/BrambleXu/KGQA_SG/security/dependabot/64) | werkzeug | Werkzeug safe_join() allows Windows special device names | 升级并锁定为 3.1.8 |
| [#65](https://github.com/BrambleXu/KGQA_SG/security/dependabot/65) | urllib3 | urllib3 streaming API improperly handles highly compressed data | 升级并锁定为 2.7.0 |
| [#66](https://github.com/BrambleXu/KGQA_SG/security/dependabot/66) | urllib3 | Decompression-bomb safeguards bypassed when following HTTP redirects (streaming API) | 升级并锁定为 2.7.0 |
| [#67](https://github.com/BrambleXu/KGQA_SG/security/dependabot/67) | werkzeug | Werkzeug safe_join() allows Windows special device names with compound extensions | 升级并锁定为 3.1.8 |
| [#68](https://github.com/BrambleXu/KGQA_SG/security/dependabot/68) | werkzeug | Werkzeug safe_join() allows Windows special device names | 升级并锁定为 3.1.8 |
| [#69](https://github.com/BrambleXu/KGQA_SG/security/dependabot/69) | flask | Flask session does not add `Vary: Cookie` header when accessed in some ways | 升级并锁定为 3.1.3 |
| [#70](https://github.com/BrambleXu/KGQA_SG/security/dependabot/70) | tornado | Tornado has incomplete validation of cookie attributes | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#71](https://github.com/BrambleXu/KGQA_SG/security/dependabot/71) | tornado | Tornado is vulnerable to DoS due to too many multipart parts | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#73](https://github.com/BrambleXu/KGQA_SG/security/dependabot/73) | pygments | Pygments has Regular Expression Denial of Service (ReDoS) due to Inefficient Regex for GUID Matching | 升级并锁定为 2.21.0 |
| [#74](https://github.com/BrambleXu/KGQA_SG/security/dependabot/74) | tornado | Tornado has cookie attribute injection via .RequestHandler.set_cookie | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#75](https://github.com/BrambleXu/KGQA_SG/security/dependabot/75) | pytest | pytest has vulnerable tmpdir handling | 升级并锁定为 9.1.1 |
| [#76](https://github.com/BrambleXu/KGQA_SG/security/dependabot/76) | tornado | Tornado has out-of-bounds memory access via C extension | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#77](https://github.com/BrambleXu/KGQA_SG/security/dependabot/77) | tornado | tornado AsyncHTTPClient accumulates decompressed chunks without size limit (gzip bomb) | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#78](https://github.com/BrambleXu/KGQA_SG/security/dependabot/78) | tornado | Tornado: Authorization header forwarded across cross-origin redirects in SimpleAsyncHTTPClient | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#79](https://github.com/BrambleXu/KGQA_SG/security/dependabot/79) | tornado | Tornado: CurlAsyncHTTPClient leaks per-request credentials on handle reuse | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#80](https://github.com/BrambleXu/KGQA_SG/security/dependabot/80) | numpy | Numpy Deserialization of Untrusted Data | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#81](https://github.com/BrambleXu/KGQA_SG/security/dependabot/81) | tornado | Tornado vulnerable to Header Injection and XSS via reason argument | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#82](https://github.com/BrambleXu/KGQA_SG/security/dependabot/82) | tornado | Tornado: Quadratic DoS via Repeated Header Coalescing | 移除；历史 notebook/爬虫已删除，不再安装 |
| [#83](https://github.com/BrambleXu/KGQA_SG/security/dependabot/83) | tornado | Tornado: Quadratic DoS via Crafted Multipart Parameters | 移除；历史 notebook/爬虫已删除，不再安装 |
