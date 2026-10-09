# 绘图智能体

这是本机科研绘图工作区。以后在此目录处理数据图、科学示意图、组图、可编辑矢量图和图件导出。

## 目录

- `input/`：本次任务的数据、参考图，或指向原文件的路径索引。不要改写原始输入。
- `output/图/`：PNG、PDF、SVG 等成图，按主题建立子目录。
- `output/脚本/`：可复现的 Python、R 或 SVG 源文件，按主题建立子目录。
- `output/表/`：分析结果表与绘图所用数据，按主题建立子目录。
- `output/报告/`：图注、方法说明、来源记录与导出检查，按主题建立子目录。
- `.codex/agents/drawing_studio.toml`：此工作区的自定义绘图 agent 配置。
- `.agents/skills/`：Tavotto 和外部科研绘图 skill 的项目级副本；许可证与分发范围见 `THIRD_PARTY_SKILLS.md`。
- `third_party/`：对应的上游仓库浅克隆/稀疏克隆；AgentFigureGallery 的源码、虚拟环境及轻量内置图库也在此。
- `.venv/`：本项目 Python 绘图/审查环境，基于本机 scientific Python 安装，并包含 Nature Figure PDF 审查所需的 PyMuPDF。
- `figures/`：Tavotto 管理的绘图脚本和同名产物目录，遵从该技能的文件契约。

## 使用

在本目录启动 Codex，或把绘图任务明确指定到此目录。直接描述目标和输入文件即可；需要专门的子 agent 时可指定 `drawing_studio`。本工作区默认使用 Python 作图；明确要求 R 时使用 R。当前本机没有 `Rscript`，R 任务需要先准备 R 环境。

在本机运行绘图和审查脚本时使用 `.venv/bin/python`。AgentFigureGallery 使用独立环境和内置轻量图库，调用方式见 `AGENTS.md` 与 `THIRD_PARTY_SKILLS.md`。

常用技能已安装在本机的 Codex 技能目录，agent 按任务选择：EasyPlot（科研数据分析与统计图）、scansci-svg（科学矢量图）、imagegen（位图生成与编辑）、Spreadsheets（工作簿）、visualize（交互图）。仓库随附 Figures for Papers、Nature Figure、AgentFigureGallery、SciPilot 和 K-Dense scientific-visualization 的项目级技能副本。Paper Plot Skills 仅在本机保留，因上游未提供许可证而不随仓库分发；需要时请从上游查看并按其条款单独安装。Tavotto 的 `tavotto-figure` 供明确需要画布微调、出版预检或保留原图规范化时调用；其内嵌画布功能还取决于 Tavotto MCP 是否在当前会话加载。

从 GitHub 克隆后，在本目录打开 Codex 即可读取 `AGENTS.md` 和项目级 `drawing_studio` 配置。EasyPlot 可从 [Rimagination/easyplot](https://github.com/Rimagination/easyplot) 安装。项目内 `.agents/skills/` 下的技能可由本项目 agent 发现；Tavotto 画布功能还需要另行安装并启用 [Tavotto 插件](https://github.com/Tavotto/Tavotto)。仓库默认忽略输入数据、生成图件和 `third_party/` 上游副本。外部技能的来源、版本和图库配置见 `THIRD_PARTY_SKILLS.md`。

每次交付应包含成图和可修改的源文件；有数据分析、误差线、统计标注或期刊要求时，补充方法与检查记录。
