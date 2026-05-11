# Content Project Specification XML Schema Reference

This document defines the XML structure for content project specifications. For software projects, use [xml-schema.md](xml-schema.md) instead.

## Top-Level Structure

```xml
<project_specification>
  <project_name>...</project_name>
  <overview>...</overview>
  <scope_boundaries>...</scope_boundaries>
  <technology_stack>...</technology_stack>
  <file_structure>...</file_structure>
  <content_architecture>...</content_architecture>
  <content_specifications>...</content_specifications>
  <content_guidelines>...</content_guidelines>
  <production_workflow>...</production_workflow>
  <third_party_integrations>...</third_party_integrations>
  <quality_verification>...</quality_verification>
  <success_criteria>...</success_criteria>
  <deliverables>...</deliverables>
  <production_notes>...</production_notes>
</project_specification>
```

Not all sections are required. Include only sections relevant to the project.

---

## Shared Sections

These sections follow the same structure as software specs.

### `<project_name>`
Single line. Format: `ProjectName - Short Description`.

### `<overview>`
3-4 paragraphs covering:
- What content this project produces (1st paragraph: purpose and value)
- Key content types and production workflow (2nd paragraph)
- Critical constraints (3rd paragraph, prefixed with `CRITICAL:`)

### `<scope_boundaries>`

```xml
<scope_boundaries>
  <in_scope>
    - 20 chapters of educational content covering venture capital fundamentals
    - Interactive quizzes (10 questions per chapter)
    - Webtoon-style visual episodes (20 episodes)
  </in_scope>
  <out_of_scope>
    - Video content production
    - Print-ready PDF formatting
    - Translation to other languages
  </out_of_scope>
  <future_considerations>
    - Advanced case study modules (Phase 2)
    - Certification exam preparation (Phase 3)
  </future_considerations>
</scope_boundaries>
```

### `<technology_stack>`
Tools and platforms for content production. Optional — skip if purely manual.

```xml
<technology_stack>
  <content_format>Markdown → HTML (static site)</content_format>
  <hosting>Vercel (static deployment)</hosting>
  <ai_tools>
    <image_generation>Gemini 2.5 Flash ($0.039/image)</image_generation>
    <research>Web search + official sources</research>
  </ai_tools>
  <design_system>b3rys dark theme (tokens.css)</design_system>
</technology_stack>
```

### `<file_structure>`
Content directory tree.

```xml
<file_structure>
content/
├── chapters/
│   ├── 01-introduction.md
│   └── 02-fundamentals.md
├── glossary.md
├── exam-summary.md
└── research/
    └── 01-research.md
web/
├── study/
│   ├── ch01.html
│   └── ch02.html
├── assets/
│   ├── study.css
│   └── tokens.css
└── index.html
</file_structure>
```

---

## Content-Specific Sections

### `<content_architecture>`
Overall content structure. Defines what types of content exist, how they're organized, and how they relate.

```xml
<content_architecture>
  <content_types>
    <type name="chapter">
      <format>Markdown → HTML</format>
      <count>20</count>
      <avg_length>3000-5000 characters</avg_length>
    </type>
    <type name="quiz">
      <format>JSON data + HTML renderer</format>
      <count>20 sets</count>
      <avg_length>10 questions per set</avg_length>
    </type>
    <type name="webtoon_episode">
      <format>HTML + AI-generated images</format>
      <count>20</count>
      <avg_length>8-12 panels per episode</avg_length>
    </type>
  </content_types>

  <structure>
    <!-- High-level organization -->
    Week 1 (intensive): Chapters 1-12 (fundamentals)
    Week 2 (online): Chapters 13-20 (advanced topics)
  </structure>

  <taxonomy>
    <!-- Categories, tags, difficulty levels -->
    <difficulty_levels>beginner, intermediate, advanced</difficulty_levels>
    <categories>legal, financial, operational, market</categories>
  </taxonomy>

  <relationships>
    <!-- How content pieces connect -->
    Each chapter → linked webtoon episode → linked quiz set
    Glossary ← referenced by all chapters
    Exam summary ← aggregated from all chapters
  </relationships>
</content_architecture>
```

### `<content_specifications>`
Templates and rules for each content type. This is where you define exactly what each piece of content should contain.

```xml
<content_specifications>
  <type name="chapter">
    <template>
      1. Why This Matters (2-3 sentences on relevance)
      2. Key Concepts (definitions, details, examples)
      3. Essential Terms (table: term, English, definition, context)
      4. Core Process/Structure (diagrams, flowcharts, tables)
      5. Case Study (1-2 real-world examples)
      6. Common Mistakes (misconception vs. correct understanding)
      7. Summary (3-line summary, keywords, exam points)
    </template>
    <format_rules>
      - Length: 3000-5000 characters for Week 1, 2000-3000 for Week 2
      - Start from beginner level, progressively deepen
      - Use analogies for abstract concepts
      - Include practical tips for each section
    </format_rules>
    <quality_criteria>
      - Learning objectives are clear and measurable
      - All terms are defined on first use
      - At least one real-world example per chapter
      - Statistics cite official sources with year
    </quality_criteria>
  </type>

  <type name="presentation_slide">
    <template>
      - Title slide: topic + subtitle + date
      - Agenda: 3-5 bullet points
      - Content slides: 1 key message per slide, max 6 lines
      - Summary slide: 3 takeaways
    </template>
    <format_rules>
      - Max 20 slides for 30-minute presentation
      - Font: min 24pt body, 36pt titles
      - One chart/image per slide maximum
    </format_rules>
  </type>
</content_specifications>
```

### `<content_guidelines>`
Style, tone, and quality standards that apply across all content types.

```xml
<content_guidelines>
  <tone_and_voice>
    - Professional but approachable
    - Use formal Korean (합니다체) for main content
    - Use casual Korean (해요체) for tips and asides
    - Avoid jargon without definition
  </tone_and_voice>

  <writing_style>
    - Sentence length: max 40 characters per sentence preferred
    - Active voice preferred over passive
    - Define technical terms on first appearance
    - Use bullet points for lists of 3+ items
  </writing_style>

  <visual_identity>
    - Color scheme: dark theme, green accent (#7ee787)
    - Image style: clean line art, soft pastel coloring
    - No text in AI-generated images (text renders poorly)
    - Image size: max 300KB, 6:4 aspect ratio
  </visual_identity>

  <terminology>
    - Maintain glossary (content/glossary.md)
    - Use Korean term first, English in parentheses
    - Consistent abbreviations: VC, LP, GP, IPO
  </terminology>
</content_guidelines>
```

### `<production_workflow>`
Step-by-step pipeline from raw research to published content.

```xml
<production_workflow>
  <phases>
    <phase name="research" order="1">
      <description>Gather and verify source material</description>
      <inputs>Topic outline, official source URLs</inputs>
      <outputs>Research notes with verified data</outputs>
      <tools>Web search, official databases</tools>
    </phase>
    <phase name="draft" order="2">
      <description>Write first draft following content_specifications template</description>
      <inputs>Research notes, content template</inputs>
      <outputs>Draft content in target format</outputs>
      <tools>Text editor, AI assistant</tools>
    </phase>
    <phase name="fact_check" order="3">
      <description>Verify all factual claims against primary sources</description>
      <inputs>Draft content</inputs>
      <outputs>Verified content with source annotations</outputs>
      <tools>Browser (direct URL verification), official databases</tools>
    </phase>
    <phase name="review" order="4">
      <description>Quality review against content_specifications criteria</description>
      <inputs>Verified content</inputs>
      <outputs>Approved content ready for publish</outputs>
    </phase>
    <phase name="publish" order="5">
      <description>Convert to final format and deploy</description>
      <inputs>Approved content</inputs>
      <outputs>Published content on target platform</outputs>
    </phase>
  </phases>

  <review_process>
    - Self-review against quality_verification checklist
    - User review before bulk production
    - CRITICAL: Produce 1 piece first → verify → establish process → produce rest
  </review_process>
</production_workflow>
```

### `<quality_verification>`
Checklists and verification procedures run before publishing.

```xml
<quality_verification>
  <checklist>
    - [ ] All statistics cite official sources with publication year
    - [ ] All reference URLs verified by direct browser access
    - [ ] No AI-generated data used without source verification
    - [ ] Content matches template structure from content_specifications
    - [ ] Terminology is consistent with glossary
    - [ ] Visual assets meet size/format requirements
  </checklist>

  <fact_check>
    <!-- When content contains factual claims -->
    - Before writing: search for primary sources, do NOT rely on AI training data
    - After writing: compare every factual claim against its cited source
    - URL verification: open EVERY reference URL in browser (no partial checks)
    - Hard-to-verify + low-importance claims: remove citation rather than guess
  </fact_check>

  <review_criteria>
    - Accuracy: all facts verifiable from cited sources
    - Completeness: all template sections filled
    - Consistency: tone, terminology, formatting uniform
    - Accessibility: appropriate for target audience level
  </review_criteria>
</quality_verification>
```

### `<deliverables>`
Final artifacts produced by this project.

```xml
<deliverables>
  <artifact name="study_pages">
    <format>HTML (static)</format>
    <location>web/study/ch01-20.html</location>
    <description>20 chapter study pages with dark theme styling</description>
  </artifact>
  <artifact name="quiz_data">
    <format>JSON</format>
    <location>web/data/quiz/ch01-20.json</location>
    <description>10 questions per chapter, multiple choice + OX + short answer</description>
  </artifact>
  <artifact name="glossary">
    <format>Markdown</format>
    <location>content/glossary.md</location>
    <description>Complete term definitions referenced across all chapters</description>
  </artifact>
</deliverables>
```

### `<production_notes>`
Practical guidance for the content producer.

```xml
<production_notes>
  <critical_paths>
    - Content template must be validated before bulk production
    - Fact-check process must be established on Chapter 1 before proceeding
  </critical_paths>
  <recommended_order>
    1. Define content_specifications templates
    2. Produce Chapter 1 as prototype
    3. Review and refine templates based on Chapter 1
    4. Bulk produce remaining chapters
    5. Cross-reference glossary and exam summary
  </recommended_order>
  <known_constraints>
    - AI-generated images cannot render Korean text reliably
    - Official statistics sites may block automated access
    - Law names may change over time (verify current name on law.go.kr)
  </known_constraints>
</production_notes>
```

---

## Section Applicability

| Section | Report | Presentation | Documentation | Education | Creative | Marketing |
|---------|--------|-------------|---------------|-----------|----------|-----------|
| overview | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| scope_boundaries | ✅ | △ | ✅ | ✅ | △ | ✅ |
| technology_stack | △ | △ | △ | ✅ | △ | △ |
| file_structure | △ | △ | ✅ | ✅ | △ | △ |
| content_architecture | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| content_specifications | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| content_guidelines | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| production_workflow | ✅ | △ | ✅ | ✅ | ✅ | ✅ |
| third_party_integrations | △ | △ | △ | △ | △ | △ |
| quality_verification | ✅ | △ | ✅ | ✅ | △ | ✅ |
| success_criteria | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| deliverables | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| production_notes | △ | △ | △ | ✅ | △ | △ |

✅ = Include, △ = Optional

---

## Writing Quality Checklist

- [ ] Content types are fully enumerated with format, count, and length
- [ ] Templates specify exact structure (section order, required elements)
- [ ] Tone and voice rules are specific enough to be consistently applied
- [ ] Production workflow phases have clear inputs, outputs, and tools
- [ ] Quality verification includes measurable criteria (not vague)
- [ ] Fact-check procedures are defined if content contains factual claims
- [ ] Visual identity rules include concrete values (colors, sizes, formats)
- [ ] Deliverables list all final artifacts with format and location
- [ ] Scope boundaries clearly state what is NOT included
- [ ] Success criteria are measurable
- [ ] Production notes include recommended order respecting dependencies
- [ ] CRITICAL constraint from overview is reflected in workflow and verification
