# 第三方绘图 Skill 安装与来源

本项目通过 `.agents/skills/` 提供项目级绘图技能副本。许可证随可分发副本保留；`third_party/` 上游源码克隆和本机环境不提交到 GitHub。

技能内容从以下上游仓库取得，版本号记录为本机安装时的提交。复制的文件遵守对应上游许可；实际使用前仍应查看来源仓库的最新条款。

| 技能 | 上游来源与版本 | 本仓库的分发范围 |
|---|---|---|
| `scientific-figure-making` | [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers)，`0ba898c` | 随附技能说明；保留 CC BY-NC 4.0 许可证副本。 |
| `plot-from-data`、`plot-from-image` | [sjkncs/paper-plot-skills](https://github.com/sjkncs/paper-plot-skills)，`cde5e84` | 本机安装副本和示例原图不随仓库分发；上游未提供许可证文件。 |
| `nature-figure`、`nature-shared` | [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)，`7d5f160` | 随附技能副本，保留 Apache-2.0 许可证。Nature 技能中引用的 Figures for Papers 示例素材不包含在仓库中。 |
| `agent-figure-gallery` | [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery)，`0b55f26` | 随附技能说明和 MIT 许可证；CLI 源码、虚拟环境和图库不包含在仓库中。 |
| `scipilot-figure-skill` | [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill)，`43098dd` | 随附技能副本和 MIT 许可证。 |
| `scientific-visualization` | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)，`92ace75` | 随附技能副本和 MIT 许可证。 |

## 本机工具

`third_party/` 和 `.venv/` 均由 `.gitignore` 排除。AgentFigureGallery 的命令行程序需要单独获取上游源码并按其说明安装依赖；本机安装位置为 `third_party/AgentFigureGallery/.venv/bin/agentfiguregallery`，图库通过 `AGENT_FIGURE_GALLERY_ROOT` 指向 `third_party/AgentFigureGallery`。当前轻量内置图库有 284 个候选，不是完整的 16,341 条参考库。

Paper Plot Skills 和 `nature-figure/assets/figures4papers/` 仅保留在当前机器。前者未提供许可证，后者的上游附带说明未授权再分发；公开仓库只保留必要的来源链接和不含这些素材的技能流程。

## 路由与质量检查

Skill 触发条件、职责边界、交接内容、QA 阶段和变更后的回归范围统一见 [`SKILL_ROUTING.md`](SKILL_ROUTING.md)。本项目默认用 Python；绘图和审查脚本优先运行 `.venv/bin/python`。该环境包含 Nature Figure PDF 检查所需的 PyMuPDF；R 环境见 `README.md`。
