# 中国校招轻量 Fork：最小改动清单

基于上游 [noamseg/interview-coach-skill](https://github.com/noamseg/interview-coach-skill)（MIT）。  
策略：**不重写 23 条命令**，只覆盖 5 个最高杠杆点；其余命令沿用上游逻辑，但受本包「全局语境」约束。

## 优先级（先改这 5 个）

| # | 上游命令 | 为什么先改 | 本包文件 |
|---|----------|------------|----------|
| 1 | `kickoff` | 不改画像，后面全偏；需校招身份、城市、行业、流程节点 | `references/kickoff-cn.md` |
| 2 | `mock` | 默认 FAANG/bar raiser；需专业面/HR/群面/无领导小组织 | `references/mock-cn.md` |
| 3 | `prep` / `research` | 数据源与面试形态偏北美；需校招官网、宣讲、国内流程 | `references/prep-research-cn.md` |
| 4 | `salary` / `negotiate` | 总包结构不同；需三方、毁约金、签字费、户口等 | `references/salary-negotiate-cn.md` |
| 5 | `stories` | STAR 可保留但需校招故事池（实习/项目/竞赛/学生工作） | `references/stories-cn.md` |

## 刻意先不改（省时间）

| 命令 | 原因 |
|------|------|
| `analyze` + 五维 rubric | 维度通用；校准时读 kickoff 的「校招生」档即可 |
| `practice` 8 阶梯子 | 追问/压力练习可复用；题面由 mock 语境带偏即可 |
| `linkedin` / `outreach` | 国内主战场常是 Boss/实习僧/宣讲；优先级低于面试转化 |
| `present` | 仅部分岗有答辩/PPT；有需求再加 |
| 英文 examples.md | 太大；用中文示例增量覆盖即可 |

## 使用方式（Cursor）

1. 对话中说明：按 **interview-coach-cn-campus** Skill 执行。
2. 说 `kickoff` 开始；状态写入项目根或本 skill 目录旁的 `coaching_state.md`。
3. （可选）另克隆上游完整仓库，需要细粒度英文协议时对照 `references/commands/*.md`；日常校招以本覆盖包为准。

## 与 campus-resume-mailer 的分工

| 工具 | 解决什么 |
|------|----------|
| `campus-resume-mailer` | 投递触达（邮件发出去） |
| `interview-coach-cn-campus` | 进面后转化（答得好、谈得清） |

## 岗位预设（已做）

| Preset | 路径 | 状态 |
|--------|------|------|
| `plc-electrical`（PLC 电气工程师） | `references/presets/plc-electrical-engineer.md` | **本仓库默认** |

暂不拆泛化的 `cn-internet` / `cn-soe`；按实际投递岗位增量加预设即可。

## 下一步（可选加深）

1. 跑一遍 `kickoff`，把简历与熟悉的 PLC 品牌写入 `coaching_state.md`  
2. 补 1 场「PLC 专业面」mock 真题笔记（面完后 `debrief`）  
3. 若要完整 fork：clone 上游后把本目录 `references/*-cn.md` 合并进对应 `commands/*.md`
