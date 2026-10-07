# Domain Pitfalls

**Domain:** Autonomous Grant Writing Pipeline (NIH R01)
**Researched:** 2026-10-07

## Critical Pitfalls

### Pitfall 1: Local LLM Quality for Long-Form Structured Writing
**What goes wrong:** 8B-parameter local models (Llama-3.1-8B, Nemotron-3-Ultra quantized) struggle with 12-page Research Strategy coherence, maintaining argument thread across sections, and NIH-specific terminology.
**Why it happens:** Training data lacks enough funded NIH grants; context window limits (even 8K-128K) don't hold full application + retrieved context; quantization degrades reasoning.
**Consequences:** Drafter produces generic, repetitive, or hallucinated content; Critic catches but can't fix; PI rejects output.
**Prevention:**
- Use section-by-section generation with explicit outline from Planner
- Heavy RAG grounding: retrieve 10-20 chunks per section
- Few-shot examples from PI's own anonymized grants in prompt
- Iterative refinement: Drafter → Critic feedback → Drafter revision (2-3 loops)
- Fallback: Allow optional API model (Claude, GPT-4) for pilot validation
**Detection:** PI feedback "too generic", "misses my field's language", "repetitive across aims"

### Pitfall 2: Compliance Rules Complexity and FOA Variability
**What goes wrong:** NIH has base rules (SF424) but each FOA/RFA adds exceptions (page limits, extra attachments, specific formatting). Hardcoded rules miss FOA-specific requirements.
**Why it happens:** 2000+ active FOAs; rules change yearly; some FOAs reference other guides.
**Consequences:** Generated application fails NIH automated validation (eRA Commons); PI gets rejection before review.
**Prevention:**
- FOA Parser agent: extracts rules from FOA PDF → structured config
- Compliance rules as external YAML (not code) — updated per FOA
- Critic validates against parsed FOA rules, not just base R01 rules
- Test against real FOA PDFs from PI partners
**Detection:** "Page limit wrong for this FOA", "Missing attachment X", "Format rejected by eRA"

### Pitfall 3: RAG Retrieval Relevance for Niche Scientific Domains
**What goes wrong:** Embeddings (all-MiniLM-L6-v2) don't capture domain-specific semantics; retrieves irrelevant chunks for specialized fields (e.g., structural biology vs. epidemiology).
**Why it happens:** General-purpose embeddings; PI PDFs use field-specific jargon; small chunk size loses context.
**Consequences:** Drafter hallucinates or writes generic text; misses key preliminary data; PI loses trust.
**Prevention:**
- Domain-adaptive embeddings: fine-tune on PI's papers (if GPU allows) or use larger model (BGE-large, E5-large)
- Hybrid retrieval: BM25 (keyword) + vector search
- Section-aware queries with field-specific prompt templates
- PI can manually tag/upload "key documents" per section
- Show retrieved chunks in UI for PI verification
**Detection:** PI says "missing my key paper", "retrieved irrelevant stuff", "doesn't know my field"

### Pitfall 4: Anonymization Failures
**What goes wrong:** Regex-based anonymization misses institution names in headers, grant numbers in acknowledgments, collaborator names in author lists.
**Why it happens:** PDF structure varies; names appear in tables, figures, references; grant numbers have multiple formats.
**Consequences:** PI data leaks to local LLM (still a policy violation); institutional IRB rejection; legal liability.
**Prevention:**
- Multi-layer: regex + spaCy NER + manual review UI
- Show PI what was detected/redacted before processing
- Conservative: redact more (entire affiliation blocks) rather than less
- Audit log of all anonymization decisions
**Detection:** PI spots unredacted name/institution in retrieved chunks

### Pitfall 5: Biosketch Format Complexity (2026 Common Form)
**What goes wrong:** 2026 format requires two-part Common Form + Supplement; specific table structures for contributions, positions, honors; 5-page limit per person.
**Why it happens:** Format changed Jan 2026; many templates outdated; table generation in python-docx is brittle.
**Consequences:** Biosketch rejected by NIH; PI manual fix needed; defeats automation value.
**Prevention:**
- Use validated python-docx template from nih-biosketch-builder patterns
- Generate as structured data → template fill → validate page count
- Test with real PI biosketches
**Detection:** "Biosketch over 5 pages", "Table formatting broken", "Wrong format version"

## Moderate Pitfalls

### Pitfall 6: Budget Justification Rules
**What goes wrong:** NIH has detailed rules per category (personnel effort %, equipment thresholds, foreign travel restrictions). Generic justification fails.
**Prevention:** Budget rules in compliance config; PI enters numbers in UI → agent writes justification text only.

### Pitfall 7: Cross-Section Consistency
**What goes wrong:** Specific Aims mention 3 aims but Research Strategy has 4; Budget includes personnel not in Biosketches; Approach references preliminary data not in Significance.
**Prevention:** Critic agent has explicit cross-reference checks; shared data model (ApplicationPlan) as single source of truth.

### Pitfall 8: Git History Noise
**What goes wrong:** Too many commits (per-agent, per-section) make history unusable; merge conflicts when PI edits.
**Prevention:** Squash commits per phase; use git notes for agent metadata; separate branches for PI edits vs agent drafts.

### Pitfall 9: Model Switching Mid-Pipeline
**What goes wrong:** Different agents use different models (e.g., Planner uses 70B, Drafter uses 8B) → tone/style inconsistency.
**Prevention:** Single model per pipeline run; configurable in config.json; document in PROJECT.md.

## Minor Pitfalls

### Pitfall 10: PDF Parsing Edge Cases
**What goes wrong:** PyMuPDF misses text in scanned PDFs, complex tables, or Unicode symbols (Greek letters in formulas).
**Prevention:** OCR fallback (tesseract) for scanned; pdfplumber for tables; warn PI about scanned docs.

### Pitfall 11: UI State Synchronization
**What goes wrong:** Long pipeline (20-30 min) → UI times out, WebSocket drops, PI loses progress.
**Prevention:** Persistent state in Orchestrator; poll-based progress; resume from last gate.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|----------------|------------|
| **Planner (FOA parsing)** | Misses FOA-specific attachments | Test against 5+ real FOAs; PI validates plan |
| **Retriever (RAG)** | Low recall for niche terms | Hybrid search; PI tags key docs; show chunks in UI |
| **Drafter (Aims)** | Generic hypotheses | Few-shot from PI's grants; PI gate after Aims |
| **Drafter (Strategy)** | Loses coherence at 12 pages | Section-by-section; outline enforced; iterative refine |
| **Critic (Compliance)** | FOA rule conflicts | FOA parser → config; test on real FOAs |
| **Formatter (DOCX)** | Page count mismatch | Render → count pages → adjust → re-render loop |
| **UI (Human gates)** | PI edits break structure | Structured edit forms (not free text); validate on save |

## Sources

- NIH R01 Application Guide updates (NOT-OD-26-018 for 2026 biosketch)
- CASRAI format guides (page limits, common errors)
- Local LLM benchmarks for long-form writing (promptquorum.com)
- LangGraph human-in-the-loop patterns
- python-docx table generation issues (GitHub issues)
- Grant writing tool post-mortems (GrantFlux, GrantCopilot blogs)
- Institutional IRB policies on AI/data privacy