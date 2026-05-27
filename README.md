# Project: tgraph

A focused, simpler clone of safishamsi/graphify. Turns a code folder into 
a queryable knowledge graph.

---

## Reference spec

The behavior we're cloning is documented in:
- `reference/GRAPHIFY_README.md` — CLI surface + behavior
- `reference/GRAPHIFY_ARCHITECTURE.md` — module breakdown + extraction schema

These describe a tool called "graphify". We are building our own simpler 
implementation called "tgraph" inspired by it.

**Do NOT attempt to fetch the original graphify source.** Work from the 
two reference files only. When in doubt, prefer simpler than the spec, 
not more elaborate. If a feature isn't in the v1 scope below, do not 
add it even if `reference/` mentions it.

---

## Scope (v1)

- **ONE language**: Python only. No TypeScript, no SQL, no anything else.
- **Input**: a directory of `.py` files
- **Outputs**: 
  - `graphify-out/graph.json` (node-link format)
  - `graphify-out/GRAPH_REPORT.md`
  - `graphify-out/graph.html` (pyvis interactive)
- **CLI**: `tgraph build <dir>` and `tgraph query <label>`

That's it. No MCP, no watch mode, no LLM extraction, no installers, 
no PR features, no Obsidian, no Neo4j.

---

## Architecture (non-negotiable)

Seven pure functions, one per module, communicating via dicts and a 
`networkx.DiGraph`. No shared state. No side effects outside `graphify-out/`.
detect → extract → build_graph → cluster → analyze → report → export
Module layout:
src/tgraph/
├── init.py
├── schema.py       # pydantic models for the extraction contract
├── detect.py       # walk dir, filter .py, respect .gitignore + .tgraphignore
├── extract.py      # tree-sitter Python → {nodes, edges}
├── build.py        # extractions → networkx.DiGraph
├── cluster.py      # louvain → tag nodes with community attr
├── analyze.py      # god nodes, surprising connections, suggested questions
├── report.py       # jinja template → GRAPH_REPORT.md
├── export.py       # graph.json + pyvis graph.html
├── query.py        # label match + n-hop neighborhood
└── cli.py          # typer entry point

One module = one responsibility = one test file in `tests/`.

---

## Extraction schema (the contract)

Every extractor function must return exactly this shape. `schema.py` 
defines pydantic models that enforce it. `build_graph()` validates 
before consuming.

```python
{
  "nodes": [
    {
      "id": str,              # unique within this extraction
      "label": str,           # human-readable name
      "source_file": str,     # path relative to project root
      "source_location": str  # e.g. "L42" or "L42-L78"
    }
  ],
  "edges": [
    {
      "source": str,          # node id
      "target": str,          # node id
      "relation": str,        # "calls" | "imports" | "uses" | "defines" | "references"
      "confidence": str       # "EXTRACTED" | "INFERRED" | "AMBIGUOUS"
    }
  ]
}
```

Confidence rules:
- `EXTRACTED` — a static analyzer can prove it (import statement, direct call)
- `INFERRED` — a human reading the code would agree (call-graph 2nd pass, name resolution)
- `AMBIGUOUS` — two humans would disagree (flag in report for review)

---

## Coding standards

- Python 3.11+
- Type hints everywhere; `from __future__ import annotations` at top of every file
- `pydantic` v2 for schema validation
- `uv` for dependency management, `pyproject.toml` only (no requirements.txt)
- `pytest` for tests, one test file per module
- `ruff` for lint + format
- No async in v1. No threading. No multiprocessing.
- Pure functions wherever possible. Side effects confined to `cli.py` and `export.py`.
- Docstrings on public functions only; no comment noise on obvious code.

---

## Dependency pinning

Tree-sitter grammar versions break extraction subtly. Pin these:

```toml
[project]
dependencies = [
    "tree-sitter==0.21.*",
    "tree-sitter-python==0.21.*",
    "networkx>=3.2",
    "pydantic>=2.5",
    "typer>=0.12",
    "pyvis>=0.3.2",
    "jinja2>=3.1",
    "pathspec>=0.12",  # for .gitignore-style matching
]
```

Do not upgrade tree-sitter without testing extraction output against 
the fixtures in `tests/fixtures/`.

---

## What I (the human) bring

You're working with someone who:
- Has 20 years of Python and enterprise engineering experience
- Works at Morgan Stanley on an agentic code-scanning platform spanning 
  700+ repos, using tree-sitter for AST extraction and Neo4j for graph storage
- Knows networkx, pydantic, typer, and tree-sitter well
- Plans to extend tgraph with SQL schema extraction in v2 to unify trading 
  agent code + database schema + Neo4j memory layer for TraderBrain

So: don't explain tree-sitter basics, don't explain why pure functions 
are good, don't pad explanations. Skip to decisions and tradeoffs. 
When I ask "why", I want the second-order reasoning, not the first.

---

## Extensibility: design for v2 without building it

I will add SQL schema extraction and possibly TypeScript in v2. Design 
the extractor dispatch so adding a new language is one new function 
plus one dispatch entry — NOT a rewrite. Specifically:

- `extract.py` should have a `_EXTRACTORS: dict[str, Callable]` registry 
  keyed on file suffix
- `collect_files()` in `detect.py` should read its accepted suffixes 
  from the registry, not hardcode them
- The schema must NOT have any Python-specific fields

Beyond that, don't pre-build v2 features. YAGNI applies hard here.

---

## What NOT to build in v1

- No MCP server (skip `serve.py` entirely)
- No watch mode (skip `watch.py`)
- No URL ingestion or PDF/video/image extraction (skip `ingest.py`)
- No caching layer (skip `cache.py` — add in v2 when extraction gets slow)
- No multi-platform skill installers
- No PR dashboard, Neo4j export, Obsidian vault, callflow HTML, SVG export
- No LLM backends or API keys — code-only extraction in v1
- No `.docx` / `.xlsx` / `.pdf` handling
- No global cross-project graph
- No git hooks

If you find yourself reaching for any of these, stop and confirm with me.

---

## Output directory contract

Everything tgraph produces goes under `graphify-out/` in the target 
project root (matching graphify's convention for muscle-memory). 
The directory layout:
graphify-out/
├── graph.json           # the graph, node-link format
├── GRAPH_REPORT.md      # the human-readable report
├── graph.html           # pyvis interactive viz
└── manifest.json        # file mtimes for incremental rebuilds (v1.5)
No other files. No subdirectories in v1.

---

## Testing discipline

- One test file per module: `tests/test_<module>.py`
- All tests are pure unit tests — no network, no FS writes outside `tmp_path`
- Fixtures live in `tests/fixtures/` as real `.py` files
- For graph-shape tests, build the graph by hand in the test rather 
  than going through `extract` — that way extractor changes don't 
  break analysis tests
- Aim for ~80% line coverage on `extract.py`, `build.py`, `analyze.py`. 
  CLI and export can be smoke-tested only.

---

## Working session protocol

When I start a new session:
1. Read this `CLAUDE.md` first
2. Read the two files in `reference/` if the session touches extraction or schema
3. Check `git log --oneline -10` to see what was done recently
4. Ask me what session number / module we're on if it's not obvious
5. Don't touch modules outside the current session's scope, even if 
   you notice issues — tell me, don't fix

After implementing each module:
1. Run its tests and confirm they pass before declaring done
2. Run `ruff check src/ tests/` and fix any issues
3. Suggest a commit message; let me commit

---

## Decisions already made (don't relitigate)

- networkx, not igraph or graph-tool. Pure Python, works everywhere.
- Louvain via `networkx.community.louvain_communities`, not Leiden. 
  Good enough for v1; can swap later.
- pyvis for HTML viz, not d3 or cytoscape. Five lines of code.
- typer, not click or argparse.
- DiGraph, not Graph. We want edge direction for `calls` and `imports`.
- pydantic v2, not dataclasses or attrs. We need validation, not just types.
- Project name is `tgraph` for now; may rebrand under Tectonic Labs later.

---

## Open questions (decide as we go)

- Whether to extract `# WHY:` / `# HACK:` / `# NOTE:` comments as 
  separate nodes (graphify does this). Probably yes in v1.5.
- How to handle Python type annotations as edges. Probably `uses` edges 
  with `INFERRED` confidence.
- Whether `__init__.py` re-exports count as `imports` edges. Probably yes.
- God node ranking: pure degree, or PageRank, or weighted degree? 
  Start with weighted degree (calls=2, imports=1), iterate after seeing real output.
  No other files. No subdirectories in v1.

---

## Testing discipline

- One test file per module: `tests/test_<module>.py`
- All tests are pure unit tests — no network, no FS writes outside `tmp_path`
- Fixtures live in `tests/fixtures/` as real `.py` files
- For graph-shape tests, build the graph by hand in the test rather 
  than going through `extract` — that way extractor changes don't 
  break analysis tests
- Aim for ~80% line coverage on `extract.py`, `build.py`, `analyze.py`. 
  CLI and export can be smoke-tested only.

---

## Working session protocol

When I start a new session:
1. Read this `CLAUDE.md` first
2. Read the two files in `reference/` if the session touches extraction or schema
3. Check `git log --oneline -10` to see what was done recently
4. Ask me what session number / module we're on if it's not obvious
5. Don't touch modules outside the current session's scope, even if 
   you notice issues — tell me, don't fix

After implementing each module:
1. Run its tests and confirm they pass before declaring done
2. Run `ruff check src/ tests/` and fix any issues
3. Suggest a commit message; let me commit

---

## Decisions already made (don't relitigate)

- networkx, not igraph or graph-tool. Pure Python, works everywhere.
- Louvain via `networkx.community.louvain_communities`, not Leiden. 
  Good enough for v1; can swap later.
- pyvis for HTML viz, not d3 or cytoscape. Five lines of code.
- typer, not click or argparse.
- DiGraph, not Graph. We want edge direction for `calls` and `imports`.
- pydantic v2, not dataclasses or attrs. We need validation, not just types.
- Project name is `tgraph` for now; may rebrand under Tectonic Labs later.

---

## Open questions (decide as we go)

- Whether to extract `# WHY:` / `# HACK:` / `# NOTE:` comments as 
  separate nodes (graphify does this). Probably yes in v1.5.
- How to handle Python type annotations as edges. Probably `uses` edges 
  with `INFERRED` confidence.
- Whether `__init__.py` re-exports count as `imports` edges. Probably yes.
- God node ranking: pure degree, or PageRank, or weighted degree? 
  Start with weighted degree (calls=2, imports=1), iterate after seeing real output.
