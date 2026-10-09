# SoilAgent-R Figure 1：第一阶段结构审阅

任务：[Issue #2](https://github.com/b619-y/drawing-studio-agent/issues/2)。2026-10-09用户认可总体结构，并要求改为yyc字体、安装真正Arial及精简文字。Twin下方已改为8个参数场符号、RTM下方已改为守恒与相平衡公式；沿用模型标题与CONC轴。最新修订按用户反馈收紧左下留白、统一标题及说明基线，将RTM公式按等号对齐。仍为待审结构草图，不是正式投稿图，也不关闭Issue。本轮不自动展开真实数据制图。

## 本轮设计

主线只出现一次：Auto-ETL → CSM ⇢ Digital Twin → RTM ↔ Decision/MOPSO。Twin占主要视觉宽度，以概念分层块体作为唯一主要焦点；其余是白底线稿。CSM→Twin是方法依据而非自动接口，用虚线表达。RTM与MOPSO的双向箭头分别表示候选请求与模型响应。

Twin没有真实尺度、井位或浓度色标，概念/非等比例说明移至caption和SVG描述。Decision保留CONC、COST、FLUX空三维坐标，不画随机点、伪造前沿或最优标记；TIME仍是第四优化目标，但不在这份空坐标示意中显示，不新增颜色映射。顶部虚线只表示用户重新设目标；底部资源条及分隔横线按最新用户要求删除，数据底座的实际职责不变。第5层不在图中。删除画面提示不意味着科学状态升级。

草图当前180 mm整宽、63 mm高，主标签至少7 pt；通用两栏整宽草图，不宣称符合某个期刊最新投稿规范。

## yyc字体修订

按EasyPlot保存的yyc字体规则，使用真正**Arial Bold**；`scansci-svg`仍为矢量制作主责，EasyPlot仅提供字体规范，不重算科学数据、不更改几何、配色、箭头或轴语义。

- 已安装Arial Regular、Bold、Italic、Bold Italic，仅安装到当前用户的字体目录，不修改系统字体或科研环境，不使用替代字体。
- 来源：[微软Core fonts原始Arial安装包](https://sourceforge.net/projects/corefonts/files/the%20fonts/final/arial32.exe/download)。包SHA256：`85297a4d146e9c87ac6f74822734bdee5f4b2a722d7eaa584b7f2cbf76f478f6`；与Ubuntu `ttf-mscorefonts-installer 3.8ubuntu2` 的原包记录一致，四个TTF的SHA256也逐一与该包的安装脚本记录对照一致。
- 实际Bold文件为`Arialbd.TTF`，Version 2.82，SHA256 `4044aa6b5bebbc36980206b45b0aaaaa5681552a48bcadb41746d5d1d71fd7b4`。字体文件及原安装包只在本机保存，不进入Git；[原始许可](https://corefonts.sourceforge.net/eula.htm)一并留存，PDF仅嵌入正文需要的字体子集。
- 此版本不含Unicode下标数字U+2080/U+2081，所以将`t₀`、`t₁`用原生可编辑`tspan`的数字与基线偏移实现；科学含义及主体位置不变，没有改用其他字体补字。
- 导出前检查真正Arial Bold及所有可见字符，导出后核对PDF字体为`Arial-BoldMT`。若缺Arial或发生字体回退，检查会失败，不静默生成替代版。
- 原DejaVu版保存在上一提交`15b1316`，可以通过Git比较和恢复，不另公开字体二进制。

## 3、4部分文字整理

前轮按`scansci-svg`局部编辑规范整理右侧；最新一轮统一全图版式，仍保留Arial Bold、配色、模型符号、空坐标语义及箭头方向：

- RTM的原`Time evolution`、`Mass checks`按最新要求替换为守恒和相平衡公式；Decision保留空坐标，`Color: CONC`已删除。
- 两条交互箭头由下方带移到RTM与MOPSO的栏间空隙：`Outputs`表示RTM模型响应，`Plans`表示MOPSO候选请求，方向不变。
- `Candidate schemes`归入Decision下方；门控状态说明放在caption/依据表，不挤在图面。
- 空坐标状态未改变，无候选点声明保留于SVG描述、caption及文档；没有因删减画面文字而增加虚构数据。
- 最终PDF六个右侧独立标签（含三轴标签）各出现一次；两行公式另作包围盒检查，与标签无碰撞。仍需目视判断箭头、轴及图形间的整体关系。

## 模型标题与轴标签精简（当前版）

按最新用户意见，撤回`b8efe86`的英文过程标题及双层主/副标题，恢复单行`1 CSM`、`2 Digital twin`、`3 RTM`、`4 MOPSO`；`0 Auto-ETL`不变。用户输入的“DG2 Twin”“MOPS O”按本图已有模型名称规范为`Digital twin`、`MOPSO`。

继续按`scansci-svg`局部编辑规范保留原生可编辑文字；图形、箭头、配色、Arial Bold及模型能力不变。删除`Color: CONC`，在原TIME坐标标签的位置放`CONC`。这只是CONC/COST/FLUX三维空占位投影的展示修改，不删减四目标计算中的TIME。

删除画面上的`STRUCTURE DRAFT`、虚线解释及`Conceptual illustration / not to scale`。概念、非等比例、非实测、无真实候选点、待审状态及虚线含义留在caption/README/SVG描述中；关系XML仍仅记录实施模块关系，不作为新版排版复刻。

此前按用户截图删除`shared-resources`整组（底部`Shared data / tools`文字与分隔横线）；最新一轮进一步收紧画幅，不删除实际共用数据/工具，也不重算科学结果。

## 八参数与RTM公式（本轮）

Twin下方列`K、K_d、α、λ、λ_active、R、v、D`，来自`2-数字孪生/skill/scripts/build_twin.py:143–146,351–425,707–714`登记的七个常规参数场加一个扩展场。只列名称，不抄历史清单里的数值。它们不是八个独立实测标量：`R/v/D`属于派生场，`v/D`可标为deferred；`λ_active`是情景增强场，不等同于所有路线的恒定反应速率，也不宣称已批准替换正式RTM输入。

RTM下方用当前direct RTM的局部守恒与线性相平衡关系：

\[
\frac{dM}{dt}=-\sum_f F_f-r,\qquad C_s=K_d C_w.
\]

`M`为控制体总Cr(VI)库存（mg），`F_f`为有符号向外面质量率（mg/d，含对流与弥散），`r`为净反应质量率（mg/d）；`C_s`只指吸附相（mg/kg），不是土壤总浓度，`C_w`为水相（mg/L），`K_d`用L/kg。依据为`3-rtm模拟/skill/scripts/rtm_mopso/mass_conservative_solver.py:215–226,547–634,815–875`。该图展示半离散守恒关系，不替代实际算子分裂、正性处理及独立质量账本；`r`由实际路线、有限容量和作用窗口决定，未将工程反应压成持续恒定`λ_active`。

公式保留原生可编辑文字，参数与相平衡下标采用`tspan`；按真正Arial Bold字宽确定起点，不对每个下标片段单独居中。无科学代码或数据改写。

## 留白、对齐与公式排版（最新修订）

按`scansci-svg`重排同一SVG：画幅由180×82 mm收紧为180×63 mm，字体物理尺寸不缩小。五个模块标题共用`y=200`基线；ETL、CSM与Twin下方说明统一为`y=550/590`两行，RTM第二式及候选输出也共用`y=590`末行基线。CSM仅将Source与Pathway合到一行，三个概念均保留。

RTM导数改为原生文字和分数横线，不栅格化或描成字形轮廓；两式等号统一在`x=1242`，右端统一在`x=1270`。最终PDF检查两行完整文字包围盒不重叠，等号位置一致。Outputs/Plans移至栏间，Candidate schemes直接归在MOPSO下方，避免右侧尾部拉高全图。关联箭头按原来源、目标及方向重接。

仅调整示意对象的尺寸、位置与文字分行；没有新增参数、修改公式含义或改变科学状态。最终PDF重渲染PNG已由绘制者及独立只读审阅者核对，无必须修正的遮挡或对齐问题；未做目标编辑器交互验证。

## 成果与来源

- [科学依据表](../../表/20261009-16-SoilAgent-R-Figure1/20261009-16-元素与科学依据.md)。
- 原生可编辑[SVG](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.svg)、矢量[PDF](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.pdf)与[PNG预览](../../图/20261009-16-SoilAgent-R-Figure1/20261009-16-系统架构-结构草图.png)，均为第一阶段草图。
- 关系结构XML与导出/QA脚本：`../../脚本/20261009-16-SoilAgent-R-Figure1/`。
- 科学来源：研究仓库main `e2e1f2b25ae9746ab3632fc118f946bf62582546`；治理文档HEAD `c287d03`。绘图仓库起点 `4700d89dd3a2c5498b5ab213ee968670e35b5c3c`。
- 仓库公开，只提交本次原创概念图、源码、来源指针和QA；不上传私有代码正文、调查表、三维场或候选数据。

## 工具与QA边界

按 `SKILL_ROUTING.md`，主责为本机 `scansci-svg`，本轮使用原生SVG构形。`drawio-skill`在第一阶段仅辅助保留关系XML及结构检查：Linux缺draw.io CLI，**没有执行draw.io图像导出/桌面编辑验证**。目视发现PyMuPDF的SVG转换丢失虚线且替换字体，故改用CairoSVG导出矢量PDF，PyMuPDF仅做PDF检查及PNG重渲染。只在绘图clone建立忽略的`.venv`；科学仓库及其运行环境未改动。本轮字体安装不调用系统级安装器；cabextract及其依赖只解压在临时工具目录。

自动检查包括SVG唯一ID、五模块唯一、禁止位图/随机点/额外Agent、箭头拓扑、原生文字、PDF物理尺寸/无图像对象、字体及虚线保留、重新渲染及源码SHA。实际回执见[QA JSON](20261009-16-结构草图-QA.json)。

- 21项回归测试通过，包含模型标题、画面注记/资源条删除、CONC轴位置、元数据状态保留、八参数、可编辑分数及对齐基线；scansci结构检查通过。最终PDF五个模型标题及六个右侧标签各出现一次、文字包围盒无碰撞，两行公式及其标签无碰撞、等号对齐，已删文字未残留。关系XML未改，上一轮drawio严格检查0错误、0警告仍适用于原文件，本轮不重复桌面导出。
- PDF为180×63 mm，原生矢量、无图像对象；仅使用`Arial-BoldMT`。主体文字最小7.37 pt，原生下标6.24 pt；字体子集嵌入，两条虚线确实保留，所有可见字符都有Arial字形。
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

1. 总体结构已获用户“还行”反馈，本轮按其最新意见改回模型标题并精简画面；后续进一步排版或数据制图需沿用已认可结构。
2. 结构批准后，选择可公开的已核验Twin几何/场素材和真实四目标候选数据，锁定运行来源SHA、门控状态、单位及使用授权。本阶段没有导入这些素材，不把“未导入”说成项目没有数据。
3. 若保持概念Twin，可继续精绘但保留非等比例声明；真实3D Pareto须有可核验输入，不能用随机数补齐。提交前再检查科学语义、版面、字体与最终PDF。

## English caption（结构草图）

**Figure 1. Evidence-grounded architecture of SoilAgent-R (structure draft pending review).** Site information is organized through Auto-ETL, a conceptual site model (CSM), three-dimensional digital-twin construction, reactive transport modelling (RTM), and multi-objective decision support (MOPSO). The CSM-to-twin connection represents methodological guidance rather than a claimed automated file interface. The Outputs and Plans links denote RTM model responses and MOPSO candidate requests, respectively. The four objectives are concentration (CONC), cumulative transport (FLUX), cost (COST), and engineering duration (TIME). The empty CONC/COST/FLUX axes are a layout placeholder without candidate points; TIME remains a fourth optimization objective but is not displayed in this placeholder. No objective-to-color mapping is shown. Candidate schemes remain screening-level and subject to formal evaluation gates, not validated engineering optima. The conceptual block is not to scale and does not encode measured concentrations. Dashed feedback denotes user revision of goals, not an autonomous real-time control loop. New reconstruction candidates are currently No-Go for replacing the retained RTM input.

The eight symbols below the twin identify documented parameter-field groups, including derived and scenario-dependent fields, not eight independently measured quantities. The RTM equations denote control-volume mass balance and equilibrium partitioning: M is total cell Cr(VI) mass, F is signed outward face mass rate, r is net reaction mass rate, and C_s and C_w are sorbed and aqueous concentrations. Engineering reaction rates retain their applicable capacity and time-window constraints.
