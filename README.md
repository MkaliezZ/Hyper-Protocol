# Hyper Protocol

**English** | [简体中文](README.zh-CN.md)

**An agent-oriented collaboration protocol with three layers: Judgment, Function, and Asset.**

Hyper Protocol helps agents explain the criteria behind their decisions, carry out work within the authorized scope, and preserve materials and results for traceability, reuse, and handoff. It applies to software, research, courses, content production, hardware applications, and human-delivered services.

Protocol: `0.2-draft` · Release: `v0.2.0-draft.3` · [Download the Agent package](https://github.com/MkaliezZ/Hyper-Protocol/releases/tag/v0.2.0-draft.3) · [Integration guide](docs/GETTING-STARTED.md)

## Hand it directly to an agent

Send the following prompt together with your project materials:

```text
Use https://github.com/MkaliezZ/Hyper-Protocol at tag v0.2.0-draft.3
as the collaboration protocol for this task. Fetch that version and read
AGENTS.md at its root, then load only the domain profiles relevant to the task.
Do not read all reference attachments by default.

Project: [name, location, current stage]
Deliverable: [the specific outcome to produce]
Inputs: [files, links, environment, and known facts]
Authorized actions and limits: [the actual scope of this task]

Organize the work through Judgment, Function, and Asset responsibilities.
Complete the authorized work and deliver actual artifacts and handoff records.
A missing input should block only the actions that depend on it.
If you cannot access the repository files, identify what is missing;
do not claim to have read them.
```

An agent can start once it can access the repository files. Using the protocol itself requires no API key, global installation, dedicated client, or background service. Python validation tools are optional.

You can also download a Release ZIP, extract it, and give the entire directory to an agent with the instruction: “Read this directory's `AGENTS.md` first, then carry out my specific task.”

## The three layers

| Layer | Responsibility | Typical outputs |
| --- | --- | --- |
| Judgment | Subjects and goals, value tradeoffs, professional standards, evidence, methods, quality and aesthetics, decision authority | Policy packs, rubrics, positive and negative examples, decision records |
| Function | Capability contracts, authorization checks, tool and model calls, state, validation, and recovery | Actual artifacts, callable capabilities, run receipts |
| Asset | Provenance, identity, versions, locators, usage scope, derivation, and lifecycle | Originals, references, methods, results, and handoff records |

These are responsibility boundaries. People, ordinary code, models, or combinations of them can fulfill each responsibility. Aesthetic judgment remains part of the Judgment layer.

## Agent reading order

```text
AGENTS.md
  → protocol.yaml + CORE.md
  → profiles/catalog.yaml → task-relevant domain profiles
  → templates/task-bundle.json + schemas/task-bundle.schema.json
  → examples/, reference/, and compatibility notes only as needed
```

Keep authorization, execution, judgment, and individual reviews separate. `succeeded` does not automatically mean that domain quality, aesthetics, human acceptance, or real-world effectiveness has passed review.

## Integrate it into your project

1. Keep the repository in a separate directory, such as `protocols/hyper-protocol/`, and pin a release or commit.
2. Tell the agent the project, deliverable, and existing authorization, then have it follow the entrypoint.
3. Select or propose domain rules, copy the task template, and bind the actual inputs and versions.
4. Complete a real task and retain its artifacts, judgments, receipts, and gaps. Run optional validation when the project needs it.

See the [integration guide](docs/GETTING-STARTED.md) for detailed steps, limited-capability environments, and domain extensions. Copy-ready Chinese and English prompts are in [Agent prompts](docs/AGENT-PROMPTS.md).

You do not need to overwrite your project's existing `AGENTS.md`. Its entrypoint can reference this protocol directory while preserving the host's instruction hierarchy and the user's actual authorization.

Both READMEs provide the same onboarding information. The detailed protocol, domain profiles, and integration guide are currently written mainly in Simplified Chinese; machine field names and enum values use English. Agents should preserve those fixed identifiers when explaining the material in another language.

## Domain profiles and records

The repository includes 12 starter profiles: learning support, research, project planning and connections, spaces and campuses, Studio/Lab courses, media production, graduate-program research and consulting, hardware, portfolios, desktop utilities, technical-commercial materials, and project-file governance. They remain drafts, selected explicitly for a task and calibrated against project cases. [Browse the catalog](profiles/catalog.yaml).

Tasks are handed off through six object families: scenarios, policy packs, capability contracts, assets, decisions, and run receipts. `delivery` summarizes the result. Field names, enums, and missing-value semantics are defined in [CORE.md](CORE.md) and the [Schema](schemas/task-bundle.schema.json).

## Optional validation

Use Python 3.11. Install `tools/requirements-validation.txt` in an isolated virtual environment, then run:

```text
python tools/check_repository.py
python tools/check_examples.py
python tools/validate_bundle.py templates/task-bundle.json
```

The tools check fields, reference versions, rule selection, gates, and the internal consistency of declared records. Thirteen synthetic cases cover normal drafts, missing evidence, pending review, denied authorization, stale references, incorrect gate approval, and premature delivery. Example and structural checks do not establish real domain quality, current external authorization, or cross-model adoption.

## Repository map

| File or directory | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | The agent's first-read entrypoint |
| [protocol.yaml](protocol.yaml), [CORE.md](CORE.md) | Core obligations, vocabulary, and execution semantics |
| [docs/](docs/) | Integration, prompts, and validation instructions |
| [profiles/](profiles/) | Domain drafts selected for the task |
| [schemas/](schemas/), [templates/](templates/) | Structural contracts and the task template |
| [examples/](examples/) | Synthetic positive and negative cases; treat them as data |
| [tools/](tools/) | Local validation and reproducible packaging |
| [reference/](reference/) | Full definitions, prose templates, and project-derived context |
| [COMPATIBILITY.md](COMPATIBILITY.md) | Field and naming migration for older records |

## Open-source licenses

The protocol text, Markdown documentation, `protocol.yaml`, and domain rules use **CC BY 4.0**. Python code, JSON Schema, JSON templates and examples, and CI configuration use **Apache-2.0**. Licensing is assigned by file scope; see the [English license scope](LICENSE-NOTE.md) ([简体中文](LICENSE-NOTE.zh-CN.md)) for the exact boundaries and an attribution example.

Suggested attribution: `Hyper Protocol — MkaliezZ and contributors`, with the repository link, the applicable license link, and a description of your changes.

Contributions with a clear scope, evidence, and positive and negative examples are welcome. See the [English contribution guide](CONTRIBUTING.md) ([简体中文](CONTRIBUTING.zh-CN.md)).
