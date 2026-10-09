# 绘图智能体工作规则

本目录是绘图任务的默认工作区。开始时读取 `input/索引.md` 和用户提供的输入；按 `SKILL_ROUTING.md` 选定主责 Skill 与阶段性复核，再读取当前任务需要的技能文件。完成后把结果写入对应的 `output/` 分类目录。

- 科研数据准备、统计分析与数据图使用 `easyplot`。本项目默认 Python；用户指定 R 时使用 R，并在运行前检查 R 环境。
- Python 绘图和审查脚本优先使用本项目 `.venv/bin/python`；它继承本机科研绘图包，并安装了 Nature Figure PDF 审查所需的 PyMuPDF。
- 工作簿整理使用 `spreadsheets:Spreadsheets`；科学示意图和可编辑 SVG 使用 `scansci-svg`；位图生成与编辑使用 `imagegen`；对话内交互图使用 `visualize:visualize`。Skill 的调用顺序、职责交接、触发条件与 QA 阶段以 `SKILL_ROUTING.md` 为准，只加载当前任务需要的技能。
- 本地项目级绘图技能位于 `.agents/skills/`。第三方来源、许可证和未随仓库分发的副本见 `THIRD_PARTY_SKILLS.md`。缺少可选 Skill 或第三方工具时，使用项目 Python/用户指定工具继续，并注明因此未执行的检查。
- AgentFigureGallery 使用本项目 `third_party/AgentFigureGallery` 下的 CLI 和图库：命令前设置 `AGENT_FIGURE_GALLERY_ROOT="$PWD/third_party/AgentFigureGallery"`，并调用 `third_party/AgentFigureGallery/.venv/bin/agentfiguregallery`。本机配置为内置参考集；若库不可用，说明原因并继续使用其他参考流程。
- 用户明确要用 Tavotto 微调 matplotlib 图、保留原图改投稿尺寸或调用 Tavotto 预检时，使用本目录 `.agents/skills/tavotto-figure/SKILL.md`。普通数据图先走 EasyPlot；Tavotto 的画布操作需要其 MCP 在当前会话可用。
- 保留实验单位、变量与单位、组别顺序、缺失值口径和原有分析结果。不得捏造观测值、样本量、误差线或显著性；仅改图时不擅自重新分析。
- 原始输入保持只读。每项任务在 `output/图/`、`output/脚本/`、`output/表/`、`output/报告/` 下使用相同主题名，便于对应；临时预览放在该主题目录内，完成后保留需要交付的文件。
- Tavotto 任务遵从其脚本与图件同目录的契约，使用本目录 `figures/`；可在 `output/报告/` 放图注与预检记录，并在输入索引中注明对应 stem。
- 按 `SKILL_ROUTING.md` 的分阶段 QA 检查数据、分析、技术导出和最终渲染；改动后只重跑受影响的下游阶段。交付时分别说明自动检查、目视检查、未执行项和仍需用户判断的科学问题。
