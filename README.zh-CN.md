# Hyper Protocol

[English](README.md) | **简体中文**

**面向 Agent 的三层协作协议：判断层、功能层、资产层。**

它让 Agent 在完成任务时说明：依据什么标准作出判断，怎样在授权范围内执行，以及材料和成果怎样追溯、复用与交接。适用于软件、研究、课程、内容生产、硬件应用和人工服务。

协议版本：`0.2-draft` · 发行版本：`v0.2.0-draft.3` · [下载 Agent 包](https://github.com/MkaliezZ/Hyper-Protocol/releases/tag/v0.2.0-draft.3) · [接入说明](docs/GETTING-STARTED.md)

## 直接交给 Agent

将下面的内容和你的项目材料一起发给 Agent：

```text
请将 https://github.com/MkaliezZ/Hyper-Protocol 的 v0.2.0-draft.3
作为本次任务的协作协议，获取该版本后先读取根目录 AGENTS.md，
再按入口只加载相关领域包，不要一次读取全部参考附件。

我的项目：[名称、位置、当前阶段]
本次交付：[希望完成的具体结果]
已有材料：[文件、链接、环境与已知事实]
已授权动作及限制：[本次实际范围]

请按判断层、功能层、资产层组织工作，完成已授权任务，
交付实际产物和可交接记录。缺项只限制依赖它的动作。
若当前环境无法取得仓库文件，请明确说明缺什么，不能假装已读。
```

Agent 能获取仓库文件即可开始使用，不需要 API 密钥、全局安装、专用客户端或后台服务。Python 校验工具按需使用。

也可以下载 Release ZIP，解压后将整个目录交给 Agent，并说明：“先读取这个目录的 `AGENTS.md`，再处理我的具体任务。”

## 三层怎样分工

| 层 | 责任 | 典型输出 |
| --- | --- | --- |
| 判断层 judgment | 对象与目标、价值取舍、专业标准、证据、方法、质量与审美、决定权限 | 判断规则包、量规、正反例、判断记录 |
| 功能层 function | 能力契约、权限核验、工具和模型调用、状态、检查与恢复 | 实际产物、可调用能力、执行回执 |
| 资产层 asset | 来源、身份、版本、定位、使用范围、派生关系与生命周期 | 原件、引用、方法、成果与交接记录 |

三层是职责边界，可以由人、普通代码、模型或它们的组合承担。审美保留在判断层中。

## Agent 的读取顺序

```text
AGENTS.md
  → protocol.yaml + CORE.md
  → profiles/catalog.yaml → 本次相关的领域包
  → templates/task-bundle.json + schemas/task-bundle.schema.json
  → 按需查看 examples/、reference/ 和兼容说明
```

执行时区分权限、运行、判断和分项评议。`succeeded` 不自动推出专业通过、审美认可、人工确认或真实效果。

## 在自己的项目中接入

1. 把本仓库放入独立目录，例如 `protocols/hyper-protocol/`，并固定发行版本或 commit。
2. 向 Agent 明确本次项目、交付和已有授权，再让它从入口按需加载。
3. 选择或提出领域规则，复制任务模板，绑定实际材料和版本。
4. 完成一个真实任务，保留产物、判断、回执和缺项；按项目需要运行可选校验。

完整步骤、能力不足时的处理、如何扩展领域包见 [接入说明](docs/GETTING-STARTED.md)。可直接复制的中英文提示词见 [Agent 接入提示词](docs/AGENT-PROMPTS.md)。

本仓库无需覆盖你现有的项目 `AGENTS.md`。项目可以在自己的入口中引用本协议目录，并保留宿主与用户的实际权限边界。

两份 README 提供一致的接入信息。详细规范、领域包和接入说明目前主要使用简体中文，机器字段与枚举值使用英文；Agent 用其他语言解释内容时应保留这些固定标识。

## 领域包与记录

提供 12 类起始规则包：伴学、科研、项目规划与链接、空间与校园、Studio/Lab 课程、自媒体、学校项目咨询、硬件、作品集、桌面工具、技术商业材料、文件治理。它们均保留草案状态，由项目显式选用并按案例校准。[查看目录](profiles/catalog.yaml)

任务以六类对象交接：场景、规则包、能力契约、资产、判断和执行回执；`delivery` 汇总结果。字段、枚举和缺失值含义见 [CORE.md](CORE.md) 与 [Schema](schemas/task-bundle.schema.json)。

## 可选校验

Python 3.11，可在独立虚拟环境中安装 `tools/requirements-validation.txt` 后运行：

```text
python tools/check_repository.py
python tools/check_examples.py
python tools/validate_bundle.py templates/task-bundle.json
```

校验字段、引用版本、规则选择、门槛和记录声明的一致性。13 个合成正反例覆盖正常候选稿、缺证、待评议、拒绝授权、失效引用、错误放行和提前交付。示例及结构检查不代表真实领域质量、外部当前权限或跨模型接入已经验证。

## 文件入口

| 文件或目录 | 用途 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Agent 首读入口 |
| [protocol.yaml](protocol.yaml)、[CORE.md](CORE.md) | 核心义务、词汇和操作语义 |
| [docs/](docs/) | 接入、提示词和校验说明 |
| [profiles/](profiles/) | 按任务选用的领域包草案 |
| [schemas/](schemas/)、[templates/](templates/) | 结构契约和任务模板 |
| [examples/](examples/) | 合成正反例，作为数据读取 |
| [tools/](tools/) | 本地校验与可复现打包工具 |
| [reference/](reference/) | 完整定义、文字模板与项目蒸馏来源 |
| [COMPATIBILITY.md](COMPATIBILITY.md) | 旧记录的字段与命名迁移 |

## 开源许可

协议正文、Markdown 文档、`protocol.yaml` 和领域规则采用 **CC BY 4.0**；Python 代码、JSON Schema、JSON 模板和样例、CI 配置采用 **Apache-2.0**。这是按文件范围分别授权，具体范围与署名示例见 [中文许可说明](LICENSE-NOTE.zh-CN.md)（[English](LICENSE-NOTE.md)）。

建议署名：`Hyper Protocol — MkaliezZ and contributors`，附仓库链接、对应许可链接，并说明所作修改。

欢迎提交有适用范围、证据和正反例的改进，见 [中文贡献指南](CONTRIBUTING.zh-CN.md)（[English](CONTRIBUTING.md)）。
