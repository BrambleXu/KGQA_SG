# KGQA_SG · 三国人物关系图谱

[![CI](https://img.shields.io/github/actions/workflow/status/BrambleXu/KGQA_SG/ci.yml?branch=master&label=CI)](https://github.com/BrambleXu/KGQA_SG/actions/workflows/ci.yml?query=branch%3Amaster)
[![Python](https://img.shields.io/badge/Python-3.14.7-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3%2B-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![ECharts](https://img.shields.io/badge/ECharts-6.1.0-AA344D?logo=apacheecharts&logoColor=white)](https://echarts.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个本地运行的三国人物关系可视化与问答工具，支持浏览关系图谱、搜索人物、查看简介，以及进行一至两层的关系问答。

## 项目概览

- 内置 122 个人物和 146 条去重关系。
- 按资料中的魏、蜀、吴、群雄阵营分组显示人物。
- 页面使用仓库内的数据和浏览器资源，不依赖 Neo4j、LTP 模型、爬虫或外部 API。
- 应用默认只监听本机，适合学习和本地演示，不是面向公网的生产服务。

## 快速开始

项目使用 [uv](https://docs.astral.sh/uv/) 管理 Python 环境和依赖。在仓库根目录执行：

```bash
uv python install
uv sync --locked --no-dev
uv run --locked --no-dev python app.py
```

然后打开 <http://127.0.0.1:5000>。

首次同步依赖需要网络；启动应用后，页面使用本地数据和静态资源。Node.js 只用于维护前端依赖，运行应用不需要安装 Node.js。

## 核心功能

### 全部关系

进入首页即可查看完整关系图。图中支持缩放和拖动；点击人物节点，或从图下方的人物列表中选择人物，可以查看人物简介和画像。

### 人物搜索

在“人物搜索”页面输入仓库内的人物姓名，例如“曹操”或“刘备”，查看该人物的直接关系。

### 关系问答

在“关系问答”页面可以查询已有关系，例如：

```text
曹操的爸爸是谁？
刘备的义弟的儿子是谁？
```

系统会返回匹配到的答案和关系路径。问答仅支持资料中已有的一至两层关系与有限的同义词，不是通用自然语言理解，也不会根据资料之外的信息推断答案。

图中箭头表示“起点是终点的某种关系”。例如：`曹嵩 → 曹操：父亲`。

## 数据边界

人物简介、画像和关系沿用历史教学资料，尚未完成逐条史料核验。阵营归属、称谓、关系完整性和简介内容可能存在错误或截断；没有匹配到关系，只说明当前资料没有记录该关系。

## 项目结构

| 路径 | 用途 |
| --- | --- |
| `app.py` | Flask 页面、JSON 接口、安全响应头和输入限制 |
| `kgqa/data.py` | 校验并只读加载本地关系、简介和画像 |
| `data/relationships.txt` | 运行时使用的规范关系数据 |
| `data/profiles.json`、`data/portraits/` | 122 份人物简介和画像 |
| `templates/graph.html`、`static/js/graph.js` | 页面结构与交互逻辑 |
| `static/vendor/` | 随仓库提供的 ECharts 资源及其许可证说明 |
| `kgqa/queries.py`、`kgqa/parser.py` | 本地查询和有限关系问句解析 |
| `neo_db/config.py`、`neo_db/import_graph.py` | 可选的 Neo4j 导入适配器 |
| `tests/` | 回归、安全和 Neo4j 导入测试 |

## 修改关系数据

修改 `data/relationships.txt` 后重启应用，页面会重新加载关系数据。页面通过 `/graph_data` 接口读取数据。

## 可选：导入 Neo4j

网页默认不使用 Neo4j。若需要导入图数据库，先同步可选依赖：

```bash
uv sync --locked --extra neo4j
```

通过环境变量提供连接信息，不要把密码写入源码或提交到仓库：

```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
# 通过安全方式设置 NEO4J_PASSWORD
uv run --locked --extra neo4j python -m neo_db.import_graph
```

导入命令会向你配置的数据库写入专用的 `KGQASGPerson` 节点和 `RELATED_TO` 边，不会清空已有数据库。执行前请确认连接地址、数据库名称和备份策略。

## 开发与检查

首次同步开发依赖并运行完整检查：

```bash
uv sync --locked --all-extras --all-groups
uv run --locked --all-extras --all-groups pytest -q
uv run --locked ruff check .
npm ci --ignore-scripts
uv run --locked python scripts/vendor_assets.py --check
npm audit
uv run --locked python scripts/audit_dependencies.py
```

维护 ECharts 资源时，修改 `package.json` 中的精确版本，执行：

```bash
npm install --ignore-scripts
uv run --locked python scripts/vendor_assets.py
```

GitHub Actions 会在 push、pull request 和每周计划任务中运行测试、代码检查、依赖审计和静态资源校验。

## License

本项目代码以 [MIT License](LICENSE) 发布。
