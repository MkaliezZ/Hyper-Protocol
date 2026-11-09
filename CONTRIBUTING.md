# Contributing to Hyper Protocol

**English** | [简体中文](CONTRIBUTING.zh-CN.md)

Contributions with a clearly defined scope are welcome through Issues and Pull Requests.

## Changes to the specification or domain rules

Describe the original requirement, proposed replacement, rationale, applicable scope, sources, and confirmation status. Include positive examples, counterexamples, and conditions under which the rule fails. Distinguish new facts, professional judgments, author preferences, and wording changes.

When changing fixed fields, enums, rule gates, or output semantics, explain the protocol version, compatibility mapping, and impact on existing records and callers. Do not change examples merely to make checks pass.

## Changes to tools

Install `tools/requirements-validation.txt` in an isolated project environment, then run:

```text
python tools/check_repository.py
python tools/check_examples.py
python tools/build_release.py
```

The final command builds a release with a manifest and checksums, then checks the extracted package. Preserve the intended behavior of both positive and negative cases when making changes.

## Submitted materials

Submit only content that can be shared publicly. Where you have the appropriate basis to use real task records, remove sensitive details or rewrite them as synthetic examples, and retain a statement of their nature. Do not submit access credentials, real learner or client profiles, or textbooks and images without permission to distribute them.

## Contribution licensing

Contributors must have the right to provide their contributions and agree to distribution under the file-specific licenses in [LICENSE-NOTE.md](LICENSE-NOTE.md). Documentation and domain rules use CC BY 4.0; code and machine-readable contracts use Apache-2.0. Identify the sources and applicable licenses of third-party content.
