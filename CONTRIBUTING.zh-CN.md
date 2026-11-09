# 贡献 Hyper Protocol

[English](CONTRIBUTING.md) | **简体中文**

欢迎以 Issue 或 Pull Request 提交有明确适用范围的改进。

## 修改规范或领域规则

说明原要求、拟替换内容、理由、适用范围、来源与确认状态，并提供正例、反例和失效条件。区分新事实、专业判断、作者偏好和表达修订。

改变固定字段、枚举、规则门槛或输出语义时，说明协议版本、兼容映射、已有记录及调用方的影响。不要仅修改样例使检查通过。

## 修改工具

在项目独立环境中安装 `tools/requirements-validation.txt`，运行：

```text
python tools/check_repository.py
python tools/check_examples.py
python tools/build_release.py
```

最后一个命令生成带清单和校验和的发行包，并检查解压后的记录。修订时保留正反例的期望行为。

## 提交材料

只提交可公开内容。真实任务记录应在有相应使用依据时脱敏或改写为合成示例，保留性质说明。不要提交访问凭据、真实学习者或客户档案、未获许可的教材和影像。

## 贡献许可

提交者应有权提供其贡献，并同意相应文件按 [LICENSE-NOTE.md](LICENSE-NOTE.zh-CN.md) 所列许可分发。修改文档和规则使用 CC BY 4.0，代码和机器契约使用 Apache-2.0。第三方内容须标明来源与适用许可。
