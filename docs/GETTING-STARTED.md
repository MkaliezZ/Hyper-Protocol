# Hyper Protocol 接入说明

本说明面向接收协议的人和 Agent。首次接入的目标是完成一个真实任务，并留下可继续工作的记录。

## 1 获取发行版

推荐使用 [v0.2.0-draft.1](https://github.com/MkaliezZ/Hyper-Protocol/releases/tag/v0.2.0-draft.1)。选择名为 `Hyper-Protocol-v0.2.0-draft.1-agent.zip` 的附件，解压后保留整个目录结构。包内附完整性清单，Release 另附 ZIP 的 SHA-256。

如果 Agent 能使用 Git，可以让它自行执行：

```text
git clone --branch v0.2.0-draft.1 --depth 1 https://github.com/MkaliezZ/Hyper-Protocol.git
```

仓库当前 `main` 可能继续变化。任务开始时记录实际 tag 或 commit；恢复任务时不要默默切换规则版本。

## 2 将它交给 Agent

发送仓库链接或提供已解压目录，并附以下内容：

```text
请读取 Hyper Protocol 根目录 AGENTS.md，并按入口加载本次相关文件。
项目：[名称、当前阶段和位置]
交付：[具体可查看或可使用的结果]
材料：[实际已有资料与环境]
授权和限制：[当前允许的动作与范围]
请完成工作；需要交接时保存 task bundle，并指出缺项和下一步。
```

仅发出协议包时，Agent 应询问具体项目或任务。已有明确任务时，Agent 应直接使用已有材料推进，真正影响结果的缺项才提问。

## 3 Agent 按能力接入

| 环境 | 可采用的方式 |
| --- | --- |
| 可读写本地文件 | 在项目独立目录保存协议，按入口读取、完成任务并保存记录 |
| 可访问网页但不能使用本地 Git | 读取该版本的 AGENTS.md 及它引用的文件；记录实际取得的内容和版本 |
| 只能接收聊天附件 | 使用平台支持的 ZIP 读取能力，或取得解压后的必要文件 |
| 无法读取提供的链接或附件 | 说明具体缺失文件，取得必要内容后继续；不得声称已读 |

网页能力不自动提供执行工具；目录存在不自动构成采用、授权或实际运行。校验器是可选工具，缺少 Python 不阻止阅读和人工填写记录。

## 4 选择规则并绑定范围

先读取 `protocol.yaml` 和 `CORE.md`，然后查看 `profiles/catalog.yaml`。按实际服务对象和任务选包；没有合适规则时，提出有范围的领域规则草案。

领域包的 `status: draft` 描述文档成熟度；`adoption: selected_for_task` 描述本次选择。记录选择依据，不把草案自行升级为 active。

需要调整的是当前人群、目标、材料、预算、设备和风格时，使用项目配置。改变通用原则或领域门槛时，另行记录规则修订和影响范围。

## 5 形成最小工作记录

复制 `templates/task-bundle.json` 到项目输出目录，并修改：

- `bundle_id`、`nature` 和 `scenario`，写明真实任务；模板状态不能当成完成记录。
- `policy_packs`，放入实际采用的规则包内容、版本和选择依据。
- `capabilities`，记录实际能力、输入输出、动作与权限。
- `assets`，保留原件、衍生物、来源、版本及本次快照。
- `decisions` 和 `runs`，按实际判断和执行填写；未发生的记录可为空。
- `delivery`，绑定实际产物，说明状态、缺项及下一步。

`null` 表示未取得或未记录，空数组表示当前无条目；两者不自动意味着“不适用”。不适用应有理由。固定字段用英文，说明和正文可以使用中文。

参考 `examples/valid/draft-feedback.json` 了解字段关联。它及其他 examples 均为合成数据，不是你项目的初始事实；不要原样继承它的人员、权限、时间或运行结果。

## 6 执行与交付

按当前授权完成任务，实际观察异步任务终态。将工程、专业、审美、人工认可与真实使用分别记录。

交付候选稿时可选择 `draft_output`，保留待评议事项；任务要求经过评议的成果时选择 `reviewed_output`，满足本次指定评议再完成。

缺证、冲突、撤权或工具失败只限制依赖它的动作。交付已完成部分，列明受影响动作和补齐方式。

## 7 可选机器校验

在本仓库根目录，使用独立环境：

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tools/requirements-validation.txt
.\.venv\Scripts\python.exe tools/check_repository.py
.\.venv\Scripts\python.exe tools/check_examples.py
.\.venv\Scripts\python.exe tools/validate_bundle.py templates/task-bundle.json
```

macOS 或 Linux：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tools/requirements-validation.txt
.venv/bin/python tools/check_repository.py
.venv/bin/python tools/check_examples.py
.venv/bin/python tools/validate_bundle.py templates/task-bundle.json
```

检查自己的记录时，将最后一个参数换成实际 JSON 文件路径。退出码 0 表示声明检查通过，1 表示记录不一致，2 表示输入或检查环境不可用。工具不会执行能力或认证真实证据。

## 8 交接与恢复

交接时提供产物、task bundle、协议及规则版本、必要来源引用和遗留事项。恢复者核对当前权限和输入变化，创建后续记录；历史回执保留当时快照。

## 9 许可与署名

可以按对应许可采用、修改和再分发文件。规范文字及领域规则使用 CC BY 4.0；代码、Schema、JSON 模板与样例使用 Apache-2.0。保留对应许可和署名，公开改编时说明修改。项目自己的数据与成果按其权属管理，采用协议不改变它们的许可。

详见 [许可范围](../LICENSE-NOTE.md) 与 [贡献说明](../CONTRIBUTING.md)。
