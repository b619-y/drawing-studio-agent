# 绘图智能体

这是本机科研绘图工作区。以后在此目录处理数据图、科学示意图、组图、可编辑矢量图和图件导出。

## 目录

- `input/`：本次任务的数据、参考图，或指向原文件的路径索引。不要改写原始输入。
- `output/图/`：PNG、PDF、SVG 等成图，按主题建立子目录。
- `output/脚本/`：可复现的 Python、R 或 SVG 源文件，按主题建立子目录。
- `output/表/`：分析结果表与绘图所用数据，按主题建立子目录。
- `output/报告/`：图注、方法说明、来源记录与导出检查，按主题建立子目录。
- `.codex/agents/drawing_studio.toml`：此工作区的自定义绘图 agent 配置。
- `.agents/skills/tavotto-figure/`：从同级 `Tavotto` 项目复制的 Tavotto 绘图技能；仅在明确使用 Tavotto 时调用。
- `figures/`：Tavotto 管理的绘图脚本和同名产物目录，遵从该技能的文件契约。

## 使用

在本目录启动 Codex，或把绘图任务明确指定到此目录。直接描述目标和输入文件即可；需要专门的子 agent 时可指定 `drawing_studio`。本工作区默认使用 Python 作图；明确要求 R 时使用 R。当前本机没有 `Rscript`，R 任务需要先准备 R 环境。

常用技能已安装在本机的 Codex 技能目录，agent 按任务选择：EasyPlot（科研数据分析与统计图）、scansci-svg（科学矢量图）、imagegen（位图生成与编辑）、Spreadsheets（工作簿）、visualize（交互图）。Tavotto 的 `tavotto-figure` 已复制到本目录，供明确需要 Tavotto 画布微调、出版预检或保留原图规范化时调用；其内嵌画布功能还取决于 Tavotto MCP 是否在当前会话加载。

从 GitHub 克隆后，在本目录打开 Codex 即可读取 `AGENTS.md` 和项目级 `drawing_studio` 配置。按需安装上述五个技能；EasyPlot 可从 [Rimagination/easyplot](https://github.com/Rimagination/easyplot) 安装。项目内的 Tavotto 技能位于 `.agents/skills/`，Codex 会在本目录发现它；使用 Tavotto 画布功能还需要另行安装并启用 [Tavotto 插件](https://github.com/Tavotto/Tavotto)。仓库默认忽略输入数据和生成图件，避免随代码一起上传。随附技能的来源与许可证见 [第三方说明](第三方说明.md)。

每次交付应包含成图和可修改的源文件；有数据分析、误差线、统计标注或期刊要求时，补充方法与检查记录。
