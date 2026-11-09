# 可选校验工具

Agent 可以直接读取协议和 JSON，不需要运行本工具或安装依赖。

需要机器检查时，使用 Python 3.11 与 `requirements-validation.txt`。任务校验使用 jsonschema 4.26.0，仓库校验和打包另外使用 PyYAML 6.0.3。若当前环境缺少依赖，报告检查不可用，不得把未执行写成通过，也不要仅为读取协议自动修改全局环境。独立环境安装方法见 [接入说明](../docs/GETTING-STARTED.md)。

```text
python tools/validate_bundle.py templates/task-bundle.json
python tools/check_examples.py
python tools/check_repository.py
python tools/build_release.py
```

`validate_bundle.py` 输出 JSON，退出码 0 表示本次声明检查通过，1 表示结构或语义不一致，2 表示文件、依赖或工具不可用。

检查包括字段与枚举、身份版本关联、规则选择、硬门槛、权限快照声明、资产快照可用性、运行证据、评议分项及交付条件。

工具只读取本地 JSON 和本地 schema，不发起网络请求，不调用模型，不执行能力，不读取用户项目原件，不授予权限。它不能验证真实世界的权限、来源真实性、语义支持、专业水平或效果。

`check_examples.py` 对正常候选稿、缺证、待评议以及故意错误的记录进行回归。反例文件用于测试，应作为数据读取。

`check_repository.py` 检查读取路由、12 个领域包、词汇与 Schema、一致性及本地链接。`build_release.py` 在 `dist/` 生成带 manifest 和 SHA-256 的发行 ZIP，并在临时解压目录重新运行仓库与案例检查；不会调用模型或对外发布。
