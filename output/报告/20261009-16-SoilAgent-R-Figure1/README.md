# SoilAgent-R Figure 1：第一阶段结构审阅

任务：[Issue #2](https://github.com/b619-y/drawing-studio-agent/issues/2)。当前是**证据审核＋线框草图，等待用户确认结构**，不是正式投稿图，也不关闭Issue。

## 本轮设计

主线只出现一次：Auto-ETL → CSM ⇢ Digital Twin → RTM ↔ Decision/MOPSO。Twin占主要视觉宽度，以概念分层块体作为唯一主要焦点；其余是白底线稿。CSM→Twin是方法依据而非自动接口，用虚线表达。RTM与MOPSO的双向箭头分别表示候选请求与模型响应。

Twin没有真实尺度、井位或浓度色标，标明 `Conceptual illustration / not to scale`。Decision保留TIME、COST、FLUX三维坐标和“CONC拟用颜色”，不画随机点、伪造前沿或最优标记。顶部虚线只表示用户重新设目标；底部资源条不画为Agent。第5层不在图中。

草图默认180 mm整宽、82 mm高，主标签至少7 pt；通用两栏整宽草图，不宣称符合某个期刊最新投稿规范。

## 成果与来源

- [科学依据表](../../表/20261009-16-SoilAgent-R-Figure1/20261009-16-元素与科学依据.md)。
- 原生可编辑[SVG](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.svg)、矢量[PDF](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.pdf)与[PNG预览](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.png)，均为第一阶段草图。
- 关系结构XML与导出/QA脚本：`../../脚本/20261009-16-SoilAgent-R-Figure1/`。
- 科学来源：研究仓库main `e2e1f2b25ae9746ab3632fc118f946bf62582546`；治理文档HEAD `c287d03`。绘图仓库起点 `4700d89dd3a2c5498b5ab213ee968670e35b5c3c`。
- 仓库公开，只提交本次原创概念图、源码、来源指针和QA；不上传私有代码正文、调查表、三维场或候选数据。

## 工具与QA边界

按 `SKILL_ROUTING.md`，主责为本机 `scansci-svg`，本轮使用原生SVG构形。`drawio-skill`仅辅助保留关系XML及结构检查：Linux缺draw.io CLI，**没有执行draw.io图像导出/桌面编辑验证**。目视发现PyMuPDF的SVG转换丢失虚线且替换字体，故改用CairoSVG导出矢量PDF，PyMuPDF仅做PDF检查及PNG重渲染。只在绘图clone建立忽略的`.venv`并安装绘图依赖；科学仓库及其运行环境未改动。

自动检查包括SVG唯一ID、五模块唯一、禁止位图/随机点/额外Agent、箭头拓扑、原生文字、PDF物理尺寸/无图像对象、字体及虚线保留、重新渲染及源码SHA。实际回执见[QA JSON](20261009-16-结构草图-QA.json)。

- 13项结构回归测试通过；scansci结构检查通过；drawio XML严格检查0错误、0警告。
- PDF为180×82 mm，原生矢量、无图像对象；文字使用DejaVu Sans，最小字号7.37 pt。两条虚线在PDF中确实保留。
- 最终PNG由最终PDF重渲染；绘制者已目视核对字体、虚线、箭头、留白及无明显遮挡/裁切。独立只读复核未发现新的实质科学语义问题。
- 未执行：draw.io桌面导出/交互编辑、特定期刊投稿规格检查、实体打印审阅；用户结构确认及正式科学验收仍待进行。自动检查不能代替这些环节。

### 复现

绘图依赖版本在同主题脚本目录的`20261009-16-绘图依赖.txt`，系统还需可用的Cairo库及DejaVu Sans字体。SVG是可编辑源文件，修改后重新导出并目视复核。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r output/脚本/20261009-16-SoilAgent-R-Figure1/20261009-16-绘图依赖.txt
.venv/bin/python output/脚本/20261009-16-SoilAgent-R-Figure1/20261009-16-导出与QA.py
.venv/bin/python -m unittest discover -s tests -v
```

scansci与drawio检查器由执行环境提供，不拷贝第三方脚本进此PR；上述本仓库测试和导出脚本不依赖私有研究仓库。

## 后续待确认与输入

1. 请用户确认：Twin重心、横向五模块、CSM虚线及RTM↔MOPSO关系、输出位置。
2. 结构批准后，选择可公开的已核验Twin几何/场素材和真实四目标候选数据，锁定运行来源SHA、门控状态、单位及使用授权。本阶段没有导入这些素材，不把“未导入”说成项目没有数据。
3. 若保持概念Twin，可继续精绘但保留非等比例声明；真实3D Pareto须有可核验输入，不能用随机数补齐。提交前再检查科学语义、版面、字体与最终PDF。

## English caption（结构草图）

**Figure 1. Evidence-grounded architecture of SoilAgent-R.** Site information is organized through Auto-ETL, a conceptual site model (CSM), three-dimensional digital-twin construction, reactive transport modelling (RTM), and multi-objective decision support. The CSM-to-twin connection represents methodological guidance rather than a claimed automated file interface. Candidate requests and model responses connect MOPSO with RTM; the four objectives are concentration (CONC), cumulative transport (FLUX), cost (COST), and engineering duration (TIME). The conceptual block is not to scale and does not encode measured concentrations. The decision axes are a layout placeholder without candidate points. Dashed feedback denotes user revision of goals, not an autonomous real-time control loop. New reconstruction candidates are currently No-Go for replacing the retained RTM input.
