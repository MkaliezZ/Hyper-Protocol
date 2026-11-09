# v0.1 到 Agent 版的迁移

本版保留判断层、功能层、资产层及原有职责。增加固定路由、字段和状态，不自动迁移任何原项目。

当前统一英文名称为 Hyper Protocol，协议标识为 hyper-protocol，包编号前缀为 HP，规则包命名空间为 hp。导入命名修订前的记录时，显式转换这些标识后重新校验引用与版本。

| v0.1 语义 | v0.2 字段或值 |
| --- | --- |
| 判断层、功能层、资产层 | judgment、function、asset |
| 场景、规则包、能力、资产、判断、执行 | scenario、policy_packs、capabilities、assets、decisions、runs |
| 满足本次条件 | meets_conditions |
| 需要证据、需要评议 | needs_evidence、needs_review |
| 不适用、不满足条件 | not_applicable、does_not_meet |
| 尚未形成判断 | not_evaluated |
| 未开始、执行中、成功 | not_started、running、succeeded |
| 失败、取消、中断 | failed、cancelled、interrupted |
| 未进行、通过、未通过、不适用 | not_run、passed、failed、not_applicable |
| 工程、专业、审美、人工认可、真实使用 | engineering、domain、aesthetic、human_acceptance、real_world |

旧字段应逐对象迁移。原记录未包含规则版本、帮助条件、权限、评议者或来源时标记未记录，不补造。

v0.1 中单数模板改为数组，支持一个任务关联多个能力、资产、判断及运行。结构扩展放入 `extensions`。

`protocol.yaml` 与 schema 使用相同词汇。语义不明时报告冲突；不得仅修改字符串让校验通过。v0.1 参考附件中的旧编号、许可建议和示例状态仍是历史上下文。
