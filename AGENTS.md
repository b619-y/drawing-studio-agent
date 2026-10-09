# 绘图智能体工作规则

本目录是绘图任务的默认工作区。先查看 `input/索引.md` 与用户提供的文件，再按图件类型读取相关技能；完成后把文件写入对应的 `output/` 分类目录。

- 科研数据准备、统计分析与数据图使用 `easyplot`。本项目默认 Python；用户指定 R 时使用 R，并在运行前检查 R 环境。
- Python 绘图和审查脚本优先使用本项目 `.venv/bin/python`；它继承本机科研绘图包，并安装了 Nature Figure PDF 审查所需的 PyMuPDF。
- Excel、CSV 等工作簿处理使用 `spreadsheets:Spreadsheets`；科学示意图、可编辑 SVG 和格式转换使用 `scansci-svg`；位图生成与编辑使用 `imagegen`；对话内交互图使用 `visualize:visualize`。只加载当前任务需要的技能。
- 本地项目级绘图技能位于 `.agents/skills/`。视觉方向未定时用 `agent-figure-gallery` 先检索参考；若本机安装了 Paper Plot Skills，复现具体论文图用 `plot-from-image`，匹配其样式模板用 `plot-from-data`；沿用 Figures for Papers 代码风格用 `scientific-figure-making`；复杂投稿多面板结构可选 `nature-figure`；不确定选图时可参考 `scipilot-figure-skill`；数据真实性、缺失/不确定性、可访问性及导出审查可参考 K-Dense 的 `scientific-visualization`。这些技能与 EasyPlot 有重叠，按任务选用，不要叠加重复的分析或质控流程。第三方来源、许可证和本地未随仓库分发的副本见 `THIRD_PARTY_SKILLS.md`。
- AgentFigureGallery 使用本项目 `third_party/AgentFigureGallery` 下的 CLI 和图库：命令前设置 `AGENT_FIGURE_GALLERY_ROOT="$PWD/third_party/AgentFigureGallery"`，并调用 `third_party/AgentFigureGallery/.venv/bin/agentfiguregallery`。本机配置为内置参考集；若库不可用，说明原因并继续使用其他参考流程。
- 用户明确要用 Tavotto 微调 matplotlib 图、保留原图改投稿尺寸或调用 Tavotto 预检时，使用本目录 `.agents/skills/tavotto-figure/SKILL.md`。普通数据图先走 EasyPlot；Tavotto 的画布操作需要其 MCP 在当前会话可用。
- 保留实验单位、变量与单位、组别顺序、缺失值口径和原有分析结果。不得捏造观测值、样本量、误差线或显著性；仅改图时不擅自重新分析。
- 原始输入保持只读。每项任务在 `output/图/`、`output/脚本/`、`output/表/`、`output/报告/` 下使用相同主题名，便于对应；临时预览放在该主题目录内，完成后保留需要交付的文件。
- Tavotto 任务遵从其脚本与图件同目录的契约，使用本目录 `figures/`；可在 `output/报告/` 放图注与预检记录，并在输入索引中注明对应 stem。
- 导出后按实际使用尺寸检查文字、单位、图例、裁切、色彩区分、字体与面板对齐。交付时说明源文件、成图、检查结果和仍需用户判断的科学问题。
