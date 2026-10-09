# SoilAgent-R Figure 1：第一阶段结构审阅

任务：[Issue #2](https://github.com/b619-y/drawing-studio-agent/issues/2)。2026-10-09用户认可总体结构，并要求改为yyc字体、安装真正Arial；随后反馈3、4部分文字混乱，并要求编号后体现过程、模型名放下行。当前完成**结构草图的字体、右侧排版与过程标题修订**，不是正式投稿图，也不关闭Issue。本轮不自动展开真实数据制图。

## 本轮设计

主线只出现一次：Auto-ETL → CSM ⇢ Digital Twin → RTM ↔ Decision/MOPSO。Twin占主要视觉宽度，以概念分层块体作为唯一主要焦点；其余是白底线稿。CSM→Twin是方法依据而非自动接口，用虚线表达。RTM与MOPSO的双向箭头分别表示候选请求与模型响应。

Twin没有真实尺度、井位或浓度色标，标明 `Conceptual illustration / not to scale`。Decision保留TIME、COST、FLUX三维坐标和“CONC拟用颜色”，不画随机点、伪造前沿或最优标记。顶部虚线只表示用户重新设目标；底部资源条不画为Agent。第5层不在图中。

草图默认180 mm整宽、82 mm高，主标签至少7 pt；通用两栏整宽草图，不宣称符合某个期刊最新投稿规范。

## yyc字体修订

按EasyPlot保存的yyc字体规则，使用真正**Arial Bold**；`scansci-svg`仍为矢量制作主责，EasyPlot仅提供字体规范，不重算科学数据、不更改几何、配色、箭头或轴语义。

- 已安装Arial Regular、Bold、Italic、Bold Italic，仅安装到当前用户的字体目录，不修改系统字体或科研环境，不使用替代字体。
- 来源：[微软Core fonts原始Arial安装包](https://sourceforge.net/projects/corefonts/files/the%20fonts/final/arial32.exe/download)。包SHA256：`85297a4d146e9c87ac6f74822734bdee5f4b2a722d7eaa584b7f2cbf76f478f6`；与Ubuntu `ttf-mscorefonts-installer 3.8ubuntu2` 的原包记录一致，四个TTF的SHA256也逐一与该包的安装脚本记录对照一致。
- 实际Bold文件为`Arialbd.TTF`，Version 2.82，SHA256 `4044aa6b5bebbc36980206b45b0aaaaa5681552a48bcadb41746d5d1d71fd7b4`。字体文件及原安装包只在本机保存，不进入Git；[原始许可](https://corefonts.sourceforge.net/eula.htm)一并留存，PDF仅嵌入正文需要的字体子集。
- 此版本不含Unicode下标数字U+2080/U+2081，所以将`t₀`、`t₁`用原生可编辑`tspan`的数字与基线偏移实现；科学含义及主体位置不变，没有改用其他字体补字。
- 导出前检查真正Arial Bold及所有可见字符，导出后核对PDF字体为`Arial-BoldMT`。若缺Arial或发生字体回退，检查会失败，不静默生成替代版。
- 原DejaVu版保存在上一提交`15b1316`，可以通过Git比较和恢复，不另公开字体二进制。

## 3、4部分文字整理

按`scansci-svg`局部编辑规范，保护0/1/2、Arial Bold、配色、模型符号和三轴几何，仅调整右侧说明与交互线的布局：

- RTM的`Time evolution`、`Mass checks`集中在其图形下方；Decision的`Color: CONC`与左侧摘要底行对齐。
- 两条交互箭头集中在独立下方带：`Outputs`表示RTM模型响应，`Plans`表示MOPSO候选请求，方向不变。
- `Candidate schemes`归入Decision下方；门控状态说明放在caption/依据表，不挤在图面。
- 空坐标状态未改变，无候选点声明保留于SVG描述、caption及文档；没有因删减画面文字而增加虚构数据。
- 最终PDF的六个独立标签各出现一次，文字包围盒无碰撞；仍需目视判断箭头、轴及图形间的整体关系。

## 1–4过程标题与模型副标题

继续按`scansci-svg`的可编辑文字规则，仅修改标题带；沿用英文论文稿和真正Arial Bold，图形、箭头、配色、0模块及科学状态不变。

| 编号与过程主标题 | 下行模型/方法 | 中文含义 |
|---|---|---|
| 1 Conceptualization | CSM | 概念建模 |
| 2 Site reconstruction | Digital twin | 场地重建 |
| 3 Reaction prediction | RTM | 反应预测 |
| 4 Plan optimization | MOPSO | 方案优化 |

第3项沿用用户指定的反应预测含义；RTM的输运职责仍在依据表和caption中保留，不改变求解能力。主标题具有独立可编辑ID，模型名居中下置；最终PDF检查标题不碰撞、四个模型名都位于对应过程下方。关系XML保留原模块名称，记录实施模块之间的关系，不作为新版标题排版的复刻。

## 成果与来源

- [科学依据表](../../表/20261009-16-SoilAgent-R-Figure1/20261009-16-元素与科学依据.md)。
- 原生可编辑[SVG](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.svg)、矢量[PDF](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.pdf)与[PNG预览](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.png)，均为第一阶段草图。
- 关系结构XML与导出/QA脚本：`../../脚本/20261009-16-SoilAgent-R-Figure1/`。
- 科学来源：研究仓库main `e2e1f2b25ae9746ab3632fc118f946bf62582546`；治理文档HEAD `c287d03`。绘图仓库起点 `4700d89dd3a2c5498b5ab213ee968670e35b5c3c`。
- 仓库公开，只提交本次原创概念图、源码、来源指针和QA；不上传私有代码正文、调查表、三维场或候选数据。

## 工具与QA边界

按 `SKILL_ROUTING.md`，主责为本机 `scansci-svg`，本轮使用原生SVG构形。`drawio-skill`在第一阶段仅辅助保留关系XML及结构检查：Linux缺draw.io CLI，**没有执行draw.io图像导出/桌面编辑验证**。目视发现PyMuPDF的SVG转换丢失虚线且替换字体，故改用CairoSVG导出矢量PDF，PyMuPDF仅做PDF检查及PNG重渲染。只在绘图clone建立忽略的`.venv`；科学仓库及其运行环境未改动。本轮字体安装不调用系统级安装器；cabextract及其依赖只解压在临时工具目录。

自动检查包括SVG唯一ID、五模块唯一、禁止位图/随机点/额外Agent、箭头拓扑、原生文字、PDF物理尺寸/无图像对象、字体及虚线保留、重新渲染及源码SHA。实际回执见[QA JSON](20261009-16-结构草图-QA.json)。

- 17项回归测试通过（原16项＋过程主标题/模型副标题层级回归）；scansci结构检查通过。最终PDF中的过程标题与方法副标题各出现一次，顺序正确、文字包围盒无碰撞。关系XML未改，上一轮drawio严格检查0错误、0警告仍适用于原文件，本轮不重复桌面导出。
- PDF为180×82 mm，原生矢量、无图像对象；仅使用`Arial-BoldMT`。主体文字最小7.37 pt，两个时间下标6.24 pt；字体子集嵌入，两条虚线确实保留，所有可见字符都有Arial字形。
- 最终PNG由最终PDF重渲染；绘制者已目视核对字体、虚线、箭头、留白及无明显遮挡/裁切。独立只读复核未发现新的实质科学语义问题。
- 未执行：draw.io桌面导出/交互编辑、特定期刊投稿规格检查、实体打印审阅；正式科学验收仍待进行。自动检查不能代替这些环节。

### 复现

绘图依赖版本在同主题脚本目录的`20261009-16-绘图依赖.txt`，Linux系统还需可用的Cairo库、Fontconfig及真正Arial Bold字体。用户安装字体后刷新其字体缓存；脚本不自动下载或分发字体。SVG是可编辑源文件，修改后重新导出并目视复核。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r output/脚本/20261009-16-SoilAgent-R-Figure1/20261009-16-绘图依赖.txt
.venv/bin/python output/脚本/20261009-16-SoilAgent-R-Figure1/20261009-16-导出与QA.py
.venv/bin/python -m unittest discover -s tests -v
```

scansci与drawio检查器由执行环境提供，不拷贝第三方脚本进此PR；上述本仓库测试和导出脚本不依赖私有研究仓库。

## 后续待确认与输入

1. 总体结构已获用户“还行”反馈，本轮处理其yyc字体、右侧文字及过程标题意见；后续进一步排版或数据制图需沿用已认可结构。
2. 结构批准后，选择可公开的已核验Twin几何/场素材和真实四目标候选数据，锁定运行来源SHA、门控状态、单位及使用授权。本阶段没有导入这些素材，不把“未导入”说成项目没有数据。
3. 若保持概念Twin，可继续精绘但保留非等比例声明；真实3D Pareto须有可核验输入，不能用随机数补齐。提交前再检查科学语义、版面、字体与最终PDF。

## English caption（结构草图）

**Figure 1. Evidence-grounded architecture of SoilAgent-R.** Site information is organized through Auto-ETL, a conceptual site model (CSM), three-dimensional digital-twin construction, reactive transport modelling (RTM), and multi-objective decision support. The CSM-to-twin connection represents methodological guidance rather than a claimed automated file interface. The Outputs and Plans links denote RTM model responses and MOPSO candidate requests, respectively. The four objectives are concentration (CONC), cumulative transport (FLUX), cost (COST), and engineering duration (TIME). Candidate schemes remain screening-level and subject to formal evaluation gates, not validated engineering optima. The conceptual block is not to scale and does not encode measured concentrations. The decision axes are a layout placeholder without candidate points. Dashed feedback denotes user revision of goals, not an autonomous real-time control loop. New reconstruction candidates are currently No-Go for replacing the retained RTM input.
