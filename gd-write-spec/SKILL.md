---
name: gd-write-spec
description: Write comprehensive XML-structured project specifications for software or content projects. Use when a user wants to create a build plan, project spec, technical specification, content plan, or detailed requirements document for an application or content project. Triggers include requests like "write a project spec", "create a build plan", "make a technical specification", "spec out this app idea", "plan my content project", "콘텐츠 기획서 작성", "write requirements for my project", or any request to produce a structured document describing what to build or create. Also use when refining or expanding an existing spec. The output is an XML-formatted .md file optimized for consumption by AI coding agents (e.g., Claude Code, Cursor, Copilot Workspace) or human developers.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "WebFetch"]
---

> **출처**: [revfactory/skills · project-spec-writer](https://github.com/revfactory/skills/tree/main/project-spec-writer) (MIT License) · 도입 시점 미기록
> 로컬 변경: 이름 `project-spec-writer` → `gd-write-spec` · 콘텐츠 프로젝트 지원 추가 (description 확장) · `allowed-tools` 명시 · `references/` 에 콘텐츠용 가이드 추가 (`example-spec-content.md`, `xml-schema-content.md`) · 다음 단계에 `gd-multi-ai-review` 권장 추가

# Project Specification Writer

Generate detailed, structured XML project specifications that serve as comprehensive build plans for software or content projects. The specs are designed to be consumed by AI coding agents or developers to build applications or produce content with minimal ambiguity.

## Workflow

### 1. Gather Project Intent

Ask the user about their project. Prioritize understanding:

1. **What** — Core purpose and key features (e.g., "a JIRA-like project management app")
2. **How** — Technical preferences: framework, language, hosting model (e.g., "React + IndexedDB, no backend")
3. **Who** — Target users and usage context
4. **Look & Feel** — Design preferences, reference apps, color themes

For **content projects**, adapt the questions:

1. **What** — Content topic and purpose (report, presentation, documentation, education, creative writing, marketing, etc.)
2. **How** — Format (document/web/slides/video/image), production tools, delivery channel
3. **Who** — Target audience, their level (expert/novice), context of consumption
4. **Look & Feel** — Tone (formal/friendly/professional), visual style, reference examples

If the user provides a brief idea, ask focused follow-up questions (max 2-3 per message) to fill gaps. If the user provides a detailed brief, proceed directly.

For **technology stack** (software), suggest sensible defaults if the user has no preference. Default toward modern, well-documented tools: React/Vite for web apps, Tailwind for styling, TypeScript for type safety.

### 2. Draft the Specification

Determine the project type and read the appropriate schema:

- **Software projects**: read [references/xml-schema.md](references/xml-schema.md)
- **Content projects**: read [references/xml-schema-content.md](references/xml-schema-content.md)
- **Hybrid projects** (content + software combined):
  1. 프로젝트의 무게중심 판단 (콘텐츠 메인? 소프트웨어 메인?)
  2. 메인 축 스키마를 기반으로 작성
  3. 보조 축 스키마에서 필요한 섹션만 가져와 추가
     - 콘텐츠 메인 + 웹앱 보조 → 콘텐츠 스키마 + `pages_and_interfaces`, `component_hierarchy`, `error_handling` 등
     - 소프트웨어 메인 + 콘텐츠 보조 → 소프트웨어 스키마 + `content_specifications`, `production_workflow`, `quality_verification` 등

Write the specification inside a single `<project_specification>` root tag. Follow this section order:

```
project_name → overview → scope_boundaries →
technology_stack → prerequisites → environment_variables → file_structure →
core_data_entities → authentication → route_definitions → component_hierarchy →
pages_and_interfaces → core_functionality → error_handling →
third_party_integrations → aesthetic_guidelines → security_considerations →
advanced_functionality → final_integration_test → success_criteria →
build_output → key_implementation_notes
```

Skip sections that don't apply to the project type (see applicability table in schema reference). For a complete example spec, see [references/example-spec.md](references/example-spec.md).

#### Writing Principles

**Be concrete, not abstract.** Every design decision should have a specific value:
- Colors: hex codes (`#1B4332`), not names ("dark green")
- Dimensions: pixel values (`56px`), not vague sizes ("large")
- Libraries: name + version (`Recharts v3.5`), not categories ("a charting library")
- Enums: list all values (`enum (Story, Bug, Task, Epic, Sub-task)`)

**Be exhaustive on data models.** Every entity needs complete field definitions with types, constraints, and relationships. Include compound indexes for any non-trivial querying patterns.

**Be specific on UI.** For each view/page, specify: layout structure, dimensions, colors, content hierarchy, interactive behaviors (hover/click/drag/keyboard), empty states, and animations with durations.

**Be opinionated on design.** Provide a complete design system: color palette (primary, background, text, status, semantic groups), typography (families with fallbacks, size scale), spacing system (base unit + scale), component styles (buttons, inputs, cards, etc.), animation specifications.

**Be actionable on implementation.** Include a recommended implementation order that respects dependency chains. Provide concrete code for schemas/configs where helpful. List critical paths that need early attention.

**Write for AI agents.** The spec consumer may be an AI coding agent. Prefer explicit, unambiguous descriptions. State architectural constraints with `CRITICAL:` prefix. Avoid prose that requires interpretation — use structured lists and specific values.

### 3. Output Format

Save as `SPEC.md` in the project root. This is the fixed filename for all project specifications.

For large specs (>500 lines), write iteratively: outline first, then fill sections one at a time.

### 4. Review and Refine

After drafting, verify against the quality checklist in the schema reference. Common gaps:
- Missing empty states for views
- Missing keyboard shortcuts
- Vague success criteria (add numbers)
- Incomplete data entity fields
- Missing dark theme colors (if theme switching is specified)
- Missing animation durations/easings
- Missing scope boundaries (what this project is NOT)
- Missing file structure tree
- Missing component hierarchy / provider wrapping order
- Missing responsive breakpoints and mobile adaptations
- Missing error handling patterns (toasts, form validation, error pages)
- Missing security considerations (input validation, CORS, rate limits)
- Missing environment variables list

Present the spec to the user and offer to expand, revise, or add detail to any section.

### 5. Extend During Project

When an existing SPEC.md needs a new domain (e.g., content project needs a web app, or software project needs content production):

1. Read the existing SPEC.md
2. Read the schema for the new domain
3. Select only the sections needed from the new schema
4. Append to the existing spec (do not rewrite existing sections)

Examples:
- Content → add software: `technology_stack` (web portion), `pages_and_interfaces`, `error_handling`
- Software → add content: `content_specifications`, `production_workflow`, `quality_verification`

For a complete content spec example, see [references/example-spec-content.md](references/example-spec-content.md).

## Section Depth Guidelines

Match detail level to project complexity:

**Software projects:**

| Project Complexity | Spec Length | Data Entities | UI Pages | Test Scenarios |
|-------------------|-------------|---------------|----------|----------------|
| Simple (todo, timer) | 200-400 lines | 2-4 entities | 2-4 views | 3-5 scenarios |
| Medium (blog, dashboard) | 400-800 lines | 5-8 entities | 5-10 views | 6-8 scenarios |
| Complex (PM tool, CRM) | 800-1700 lines | 8-15 entities | 10-20 views | 10-15 scenarios |

**Content projects:**

| Content Complexity | Spec Length | Content Types | Pieces | Verification Items |
|-------------------|-------------|---------------|--------|-------------------|
| Simple (blog, docs) | 150-300 lines | 1-2 types | 5-10 | 3-5 items |
| Medium (course, guide) | 300-600 lines | 3-5 types | 10-20 | 6-10 items |
| Complex (curriculum, multi-format) | 600-1200 lines | 5-10 types | 20+ | 10-15 items |

**Hybrid projects:** Use the main-axis complexity table + 100-200 lines for supplementary sections from the other schema.

## Adaptation for Non-Web Projects

For API/backend projects: Replace `pages_and_interfaces` with `<api_endpoints>` listing routes, methods, request/response schemas, auth requirements, and error codes.

For CLI tools: Replace `pages_and_interfaces` with `<commands_and_flags>` listing commands, arguments, flags, output formats, and interactive prompts. Replace `aesthetic_guidelines` with `<output_formatting>` for terminal output styling.

For libraries/SDKs: Replace `pages_and_interfaces` with `<public_api>` listing exported functions, classes, types, and usage examples. Replace `aesthetic_guidelines` with `<api_design_principles>`.

For content projects (reports, presentations, education, creative writing, marketing): Replace `core_data_entities` with `<content_architecture>` listing content types, structure, taxonomy, and relationships. Replace `pages_and_interfaces` with `<content_specifications>` listing templates, format rules, and quality criteria per content type. Replace `aesthetic_guidelines` with `<content_guidelines>` covering tone, writing style, visual identity, and terminology. Replace `core_functionality` with `<production_workflow>` defining phases from research through publish. Replace `final_integration_test` with `<quality_verification>` defining checklists and review criteria. Replace `build_output` with `<deliverables>` listing final artifacts and formats. Skip: `authentication`, `route_definitions`, `component_hierarchy`, `error_handling`, `security_considerations`.

## 다음 단계

SPEC.md 완성 후:

1. **(권장 — 큰 spec) 외부 모델 교차검증** — `gd-multi-ai-review` 스킬이 설치돼 있다면, SPEC 의 가정·누락·시장 적합성을 Gemini + Codex 로 cross-check. 잘못된 spec 은 구현 단계에서 비용 폭발하므로 spec 검증이 가장 cost-effective.
2. **프로젝트 골격 생성** — `/gd-start-project` 로 TODO.md / CLAUDE.md / MEMORY.md / README.md 세팅.
