# Example Spec: V-UP Education Content (Hybrid Project)

This is a reference example showing how a completed spec looks for a "Medium" complexity **content project with web application supplement**. Based on a real education content production project.

---

```xml
<project_specification>

<project_name>V-UP - Venture Capital Professional Training Content</project_name>

<overview>
V-UP is an educational content project for Korea's 61st Venture Capital Professional Training Program. It produces pre-study and review materials across multiple formats: markdown textbooks, interactive webtoon episodes, and web-based quiz applications.

Key deliverables: 20-chapter learning guide covering VC fundamentals and sector-specific investing, 20 webtoon episodes with character-driven storytelling, interactive quiz/flashcard/mock exam web apps, and a 300+ term glossary.

CRITICAL: All factual claims (statistics, legal citations, institutional descriptions) must be verified against primary sources before publication. AI training data must never be used as a factual source — always verify via official government press releases, law.go.kr, or institutional websites.
</overview>

<scope_boundaries>
  <in_scope>
    - 20 chapters of educational content (markdown → HTML)
    - 300+ term glossary with Korean/English definitions
    - 20 webtoon episodes (HTML/CSS, emoji characters)
    - Interactive quiz web app (per-chapter + mock exam)
    - Flashcard and vocabulary matching web apps
    - Exam preparation summary guide
    - Static web hosting (Vercel)
  </in_scope>
  <out_of_scope>
    - Video content production
    - Native mobile apps
    - User accounts or authentication
    - Translation to other languages
    - Print-ready PDF formatting
    - Real-time collaboration features
  </out_of_scope>
  <future_considerations>
    - AI-generated illustration replacement for emoji characters (Phase 2)
    - Spaced repetition algorithm for flashcards (Phase 2)
    - Performance analytics dashboard (Phase 3)
  </future_considerations>
</scope_boundaries>

<technology_stack>
  <content_format>Markdown (source) → HTML (published)</content_format>
  <hosting>Vercel (static deployment)</hosting>
  <dev_server>Python 3 http.server (port 8080)</dev_server>
  <ai_tools>
    <research>Google Custom Search API (Korean VC domain)</research>
    <image_generation>Gemini image model (low-res validation first)</image_generation>
  </ai_tools>
  <design_system>
    - base.css (typography, colors)
    - components.css (buttons, cards, forms)
    - tokens.css (design tokens/variables)
    - study.css (study page specific)
    - webtoon.css (webtoon specific)
  </design_system>
</technology_stack>

<file_structure>
content/
├── chapters/               # 20 chapter markdown files
│   ├── 01-vc-overview.md
│   ├── 02-investment-methods.md
│   └── ...
├── stories/                # Webtoon scenario scripts
│   ├── ep01-vc-overview.md
│   └── ...
├── research/               # Research reference data
│   ├── 01-research.md
│   └── ...
├── glossary.md             # 300+ term unified glossary
└── exam-summary.md         # Exam preparation guide

web/
├── index.html              # Landing page / dashboard
├── quiz.html               # Interactive quiz engine
├── exam.html               # Mock exam (60 questions)
├── flashcards.html         # Spaced repetition cards
├── matching.html           # Vocabulary matching game
├── study/                  # Per-chapter study pages
│   ├── ch01.html
│   └── ...
├── webtoon/
│   ├── index.html          # Episode hub
│   ├── ep01.html           # Episode 1
│   ├── ...
│   ├── images/ep01/        # Per-episode images
│   └── assets/webtoon.css
├── data/
│   ├── chapters.json       # Chapter metadata
│   ├── quiz-01.json        # Per-chapter question banks
│   ├── ...
│   ├── exam-mock.json      # Full mock exam dataset
│   └── glossary.json
└── assets/
    ├── base.css
    ├── components.css
    ├── tokens.css
    └── study.css
</file_structure>

<content_architecture>
  <content_types>
    <type name="chapter">
      <format>Markdown → HTML</format>
      <count>20</count>
      <avg_length>3000-5000 chars (Week 1), 2000-3000 chars (Week 2)</avg_length>
    </type>
    <type name="quiz_bank">
      <format>JSON data</format>
      <count>20 sets + 1 mock exam</count>
      <avg_length>10-15 questions per chapter, 60 for mock exam</avg_length>
    </type>
    <type name="webtoon_episode">
      <format>HTML + CSS + emoji characters</format>
      <count>20 episodes</count>
      <avg_length>8-12 panels per episode</avg_length>
    </type>
    <type name="glossary">
      <format>Markdown + JSON</format>
      <count>1 unified file</count>
      <avg_length>300+ terms</avg_length>
    </type>
  </content_types>

  <structure>
    Week 1 (intensive, 5 days): Chapters 1-12 — VC fundamentals, legal, valuation, fund operations
    Week 2 (online, 3 days): Chapters 13-20 — Sector-specific investing (bio, AI, culture, deeptech)
  </structure>

  <taxonomy>
    <difficulty>beginner → intermediate → advanced (progressive within each chapter)</difficulty>
    <categories>legal, financial, operational, sector-specific</categories>
  </taxonomy>

  <relationships>
    Each chapter → linked webtoon episode → linked quiz set
    Glossary ← referenced by all chapters (terms indexed by first appearance)
    Exam summary ← aggregated from all chapters (exam-critical points)
  </relationships>
</content_architecture>

<content_specifications>
  <type name="chapter">
    <template>
      1. Why This Matters — 2-3 sentences on relevance to VC practice
      2. Key Concepts — definitions, details, examples per concept
      3. Essential Terms — table: term | English | definition | practical context
      4. Core Process/Structure — diagrams, flowcharts, comparison tables
      5. Case Study — 1-2 real-world Korean VC examples
      6. Common Mistakes — misconception vs. correct understanding
      7. Summary — 3-line summary, keywords, exam-critical points
      8. Practice Questions — 5 multiple choice + 3 OX + 2 short answer
    </template>
    <format_rules>
      - Start from beginner level, progressively deepen
      - Use analogies for abstract concepts (e.g., fund structure as apartment building)
      - Include practical tips marked with 💡
      - All statistics must cite official source with year
    </format_rules>
    <quality_criteria>
      - Learning objectives are clear and measurable
      - All terms defined on first use
      - At least one real-world Korean example per chapter
      - Practice questions cover all key concepts
    </quality_criteria>
  </type>

  <type name="webtoon_episode">
    <template>
      - Opening: scene-setting narration (1-2 panels)
      - Conflict: character encounters a VC concept challenge (3-4 panels)
      - Info panel: concept explanation with visual aids (1-2 panels)
      - Resolution: character applies knowledge (2-3 panels)
      - Cliffhanger: preview of next episode topic (1 panel)
    </template>
    <format_rules>
      - Characters represented by emoji + CSS (no illustration required)
      - Max 12 panels per episode
      - One interactive quiz embedded mid-story
      - Vertical scroll layout, max-width 720px
    </format_rules>
  </type>

  <type name="quiz_bank">
    <template>
      - Multiple choice: 4 options, 1 correct, explanation for each option
      - OX (true/false): statement + explanation
      - Short answer: question + model answer + grading criteria
    </template>
    <format_rules>
      - 10-15 questions per chapter
      - Difficulty distribution: 40% basic, 40% applied, 20% challenging
      - Mock exam: 60 questions, 90-minute time limit
    </format_rules>
  </type>
</content_specifications>

<content_guidelines>
  <tone_and_voice>
    - Professional but approachable
    - Formal Korean (합니다체) for main content
    - Casual Korean (해요체) for tips and webtoon dialogue
    - Explain jargon before using it
  </tone_and_voice>

  <writing_style>
    - Sentence length: max 40 characters preferred
    - Active voice over passive
    - Define technical terms on first appearance
    - Bullet points for lists of 3+ items
  </writing_style>

  <visual_identity>
    - Study pages: dark theme, green accent (#7ee787)
    - Webtoon: light backgrounds (#F5F5F5), white speech bubbles
    - Info panels: blue-tinted (#E3F2FD)
    - Quiz panels: purple-tinted (#EDE7F6)
    - Font: Pretendard, system-ui fallback
  </visual_identity>

  <terminology>
    - Maintain unified glossary (content/glossary.md)
    - Korean term first, English in parentheses
    - Consistent abbreviations: VC, LP, GP, IPO, PEF, RCPS
  </terminology>
</content_guidelines>

<production_workflow>
  <phases>
    <phase name="research" order="1">
      <description>Web search for primary sources per topic</description>
      <inputs>Topic outline, official source URLs</inputs>
      <outputs>Research notes with verified data in content/research/</outputs>
      <tools>Google Custom Search API, official government sites</tools>
    </phase>
    <phase name="draft" order="2">
      <description>Write chapter following content_specifications template</description>
      <inputs>Research notes, chapter template</inputs>
      <outputs>Draft markdown in content/chapters/</outputs>
    </phase>
    <phase name="fact_check" order="3">
      <description>Verify all statistics, legal citations, and URLs</description>
      <inputs>Draft content</inputs>
      <outputs>Verified content with source annotations</outputs>
      <tools>Browser (direct URL verification), law.go.kr, korea.kr</tools>
    </phase>
    <phase name="web_build" order="4">
      <description>Convert to HTML study pages, generate quiz JSON, build webtoon HTML</description>
      <inputs>Verified chapters, quiz data, webtoon scenarios</inputs>
      <outputs>Static HTML/CSS/JSON in web/</outputs>
    </phase>
    <phase name="review" order="5">
      <description>Quality review against checklists, cross-reference glossary</description>
      <inputs>All built content</inputs>
      <outputs>Published content ready for deployment</outputs>
    </phase>
  </phases>

  <review_process>
    - CRITICAL: Produce Chapter 1 end-to-end first → verify → establish process → produce rest
    - Self-review against quality_verification checklist
    - User review before bulk production
  </review_process>
</production_workflow>

<quality_verification>
  <checklist>
    - [ ] All statistics cite official sources with publication year
    - [ ] All reference URLs verified by direct browser access
    - [ ] No AI-generated data used without source verification
    - [ ] Content matches template structure
    - [ ] Terminology consistent with glossary
    - [ ] Practice questions cover all key concepts (min 10 per chapter)
    - [ ] Webtoon episodes match chapter topics
    - [ ] Quiz JSON validates and renders correctly
    - [ ] All web pages responsive on mobile
  </checklist>

  <fact_check>
    - Before writing: search primary sources, never rely on AI training data
    - After writing: compare every factual claim against cited source
    - URL verification: open EVERY reference URL in browser
    - Hard-to-verify + low-importance claims: remove citation, mark as [업계 일반]
  </fact_check>

  <source_types>
    - [정부 통계] — government agency press releases
    - [법률] — verified on law.go.kr
    - [기관 공식] — institutional website confirmation
    - [업계 일반] — industry standard practice, no link needed
    - [가상 사례] — fictional case for educational purposes
  </source_types>
</quality_verification>

<success_criteria>
  <content_completeness>
    - 20 chapters fully written with all template sections
    - 300+ terms in glossary with chapter index
    - 10+ practice questions per chapter
    - 20 webtoon episodes with interactive elements
    - Complete exam preparation summary
  </content_completeness>
  <content_quality>
    - All statistics verified against primary sources
    - Zero broken reference URLs
    - Consistent terminology across all content
    - Progressive difficulty within each chapter
  </content_quality>
  <web_functionality>
    - All HTML pages load and function correctly
    - Quiz scoring works accurately
    - Mock exam respects time limits
    - Flashcard progress saves to localStorage
    - Mobile responsive on all pages
  </web_functionality>
</success_criteria>

<deliverables>
  <artifact name="study_chapters">
    <format>Markdown (source) + HTML (published)</format>
    <location>content/chapters/ + web/study/</location>
    <description>20 chapter learning guides</description>
  </artifact>
  <artifact name="webtoon_episodes">
    <format>HTML + CSS</format>
    <location>web/webtoon/ep01-20.html</location>
    <description>20 interactive webtoon episodes</description>
  </artifact>
  <artifact name="quiz_system">
    <format>JSON + HTML</format>
    <location>web/data/quiz-*.json + web/quiz.html</location>
    <description>Per-chapter quizzes + mock exam</description>
  </artifact>
  <artifact name="supplementary_apps">
    <format>HTML + JavaScript</format>
    <location>web/flashcards.html, web/matching.html</location>
    <description>Flashcard and vocabulary matching games</description>
  </artifact>
  <artifact name="glossary">
    <format>Markdown + JSON</format>
    <location>content/glossary.md + web/data/glossary.json</location>
    <description>300+ term unified glossary</description>
  </artifact>
</deliverables>

<production_notes>
  <critical_paths>
    - Chapter template must be validated on Chapter 1 before bulk production
    - Fact-check process must be established early — AI hallucinated statistics cost significant rework
    - Webtoon episode format validated on Episode 1 before scaling
  </critical_paths>
  <recommended_order>
    1. Define chapter template + write Chapter 1 as prototype
    2. Review and refine template based on Chapter 1
    3. Build study page HTML for Chapter 1 (validate web format)
    4. Produce Week 1 chapters (1-12) — exam priority
    5. Build quiz JSON + quiz web app
    6. Produce webtoon episodes for Week 1
    7. Produce Week 2 chapters (13-20)
    8. Build remaining web apps (flashcards, matching, mock exam)
    9. Cross-reference glossary and exam summary
    10. Final quality verification pass
  </recommended_order>
  <known_constraints>
    - AI-generated images render Korean text poorly (as of 2026.03) — use HTML/CSS overlay
    - Official statistics sites may block automated access — manual browser verification needed
    - Law names may change over time — verify current name on law.go.kr
    - Image generation API costs can spike — validate at low resolution first
  </known_constraints>
</production_notes>

</project_specification>
```
