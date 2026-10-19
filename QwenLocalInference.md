# Qwen Local Inference — Combined Reference

> **What this is.** One reorganized, de-duplicated merge of two EventMarketDB documents, made
> 2026-10-19. Each fact appears once, in the section where you would look for it; nothing
> important was dropped.
>
> | Source | Dated | Status in the source repo |
> |---|---|---|
> | `.claude/plans/Drivers/FinalDesign/LeftOverSteps/QwenInference.md` — **"the ledger"** | 2026-08-20 | **Current.** The only current Qwen document; wins every conflict. |
> | `.claude/plans/Drivers/FinalDesign/QwenTests/LOCAL_QWEN_HANDOFF.md` — **"the handoff"** | 2026-07-24 | **Historical.** Superseded by the ledger. Its still-valid content is merged below (tagged *handoff*); its stale advice is listed in §14.2 beside the current rule. |
>
> In EventMarketDB the ledger file remains the authority; this copy does not replace it. Relative
> paths are relative to the EventMarketDB repo root.
>
> **Placeholders** (internal details removed because this repo is public): `<REPO>` = the
> EventMarketDB repo root on the Minisforum · `<MINISFORUM_IP>`, `<MAC_IP>` = LAN addresses ·
> `<MAC_HOSTNAME>` = the Mac's mDNS name · `<user>`, `<mac-user>` = account names.

> **Live check, 2026-10-19** — added here; not in either source. Read-only queries to the Mac's
> Ollama found:
> - Installed: `qwen3.8:27b-mlx` (18.2 GB) and `qwen3.8:27b-mtp-q4_K_M` (17.7 GB). Nothing loaded.
> - Ollama **0.34.2**, not the 0.32.13 recorded in §5.3. By the ledger's own rule (§4.2), priming
>   and every suite result now need re-verification.
> - `config/local_llm.py` still defaults to `qwen3.8:27b-mlx`; its sha256 still starts `836e5722`.

## Contents

**A. Where things stand**
1. [Status](#1-status--as-of-2026-08-20)
2. [What is authoritative — read first](#2-what-is-authoritative--read-first)

**B. Setup**

3. [Machines and server](#3-machines-and-server)
4. [Models](#4-models)
5. [The client: `config/local_llm.py`](#5-the-client-configlocal_llmpy)

**C. Making a call**

6. [Graded-call contract](#6-graded-call-contract)
7. [Capacity, pre-call safety and speed](#7-capacity-pre-call-safety-and-speed)
8. [Caching and priming](#8-caching-and-priming)

**D. Rules and reference**

9. [Model-neutral qualification](#9-model-neutral-qualification)
10. [Repository rules and workflow](#10-repository-rules-and-workflow)
11. [Known defects (D1–D12)](#11-known-defects-d1d12)
12. [Results registry](#12-results-registry)
13. [History](#13-history)
14. [Retired advice — never follow](#14-retired-advice--never-follow)
15. [Artifact index](#15-artifact-index)
16. [Update template](#16-update-template)

---

## 1. Status — as of 2026-08-20

**Qwen runs no Driver role today and is not authorized for the unfinished Step 1 run.** No
diagnostic result in this document changes that.

**Authority.** Under the 2026-08-14 first-release ruling, every still-unrun model call in
Steps 1–13 is **Sonnet 5 at high effort**. Qwen enters a role only through a later owner ruling
plus its own one-role-at-a-time qualification. A passing diagnostic activates Qwen nowhere.

| State | Detail |
|---|---|
| **Proven** | Development evidence with opened keys — diagnostic, not certification (table below). |
| **Inactive** | No Qwen model runs any production or experiment role, and nothing is scheduled. A model was last recorded resident on the Mac so a future authorized run would not pay a cold load; whether it still is stays **UNKNOWN** until a read-only preflight checks. |
| **Blocked** | The client performs **no genuine pre-call token check** (§7.3). Until a later task measures the final frozen prompts and chooses the smallest safe pre-call check, no run may accept an input near the capacity limit. |
| **Planned, not started** | One temporary, read-only transport check on the frozen K-fields **196-item** packet: measure every exact prompt, report which fit the conservative safe limit, and draft the smallest `L.generate()` adapter. Awaiting the packet paths and hashes from Codex. |
| **UNKNOWN** | The 196-item packet's paths, hashes and prompt sizes. A stale **168-item** packet exists and must not be used. |
| **Next action** | Wait for Codex to supply the frozen 196-item packet paths and hashes. Take no other Qwen action. |

| Proven suite | Result | Date |
|---|---|---|
| choice_v2 table cell choice, 93 cases | 93/93, precision 1.0 | 2026-08-16/17 |
| choice_v2 compact encoding, 93 cases | 93/93, precision 1.0, 5.3 min | 2026-08-17 |
| row_v3 row selection, 93 cases | 93/93, precision 1.0 | 2026-08-16 |
| qf01 aligned 5x50 contract, 19 set-calls | 19/19 (scorer emitted the historical label `QWEN_ONLY_QUALIFIED`) | 2026-08-17 |
| Identity judge, K-pairs v1.3, 160 pairs | 157/160; 0 wrong-SAME; gate PASS | 2026-08-17 |
| Reader EXP-2 proxy, 10 of 40 chunks | either-recall 50.0% vs Sonnet 45.3% | 2026-08-17 |

Full details: §12.

### Parallel-work trigger (Codex ruling, 2026-08-20)

Qwen may start working in parallel **immediately after A4**: once the detailed answer key **and**
the Sonnet baseline are independently locked. **Verify this; do not assume it.**

- A4 is complete when a locked key and its lock file appear in
  `.claude/plans/Drivers/experiments/keys/K-fields/`, in the same shape as
  `K-pairs.v1.3.jsonl` + `.lock.json` and `K-reader.v3.jsonl` + `.lock.json`.
- On 2026-08-20 that directory held only `protocol.md`, `drafting_wrapper.md`, `draft_inputs/`
  and `draft_inputs.hashes.json` — **no key, no lock**, so the trigger had not fired.

Once it fires, in this order:

1. fix **and prove** the oversized-input pre-call blocker (§7.3);
2. build the thin local adapter (§6);
3. run only the final prompts that fit the conservative safe limit (§7.1).

The trigger does not override the standing prerequisites: the frozen 196-item packet and its
hashes must arrive first (never the stale 168-item packet), and a temporary read-only transport
check must measure every exact prompt before anything is built.

---

## 2. What is authoritative — read first

Before any Qwen work, read these completely, in order:

1. `AGENTS.md` (repo root) — communication rules, scope discipline, evidence rules.
2. The ledger, top to bottom — the only *current* Qwen-specific document.
3. `config/local_llm.py` — the live client. **Read the code; never trust a summary of it**,
   including the one in §5.
4. `.claude/plans/Drivers/FinalDesign/LeftOverSteps/Steps.md`, sections "Model-neutral AI-task
   rule" and "First-release model ruling" — the authority on whether Qwen may run at all.
5. `.claude/plans/Drivers/FinalDesign/LeftOverSteps/promptStandard.md` — how prompts are built.

Ground rules:

- Every other Qwen README, handoff, runbook and investigation note is **historical evidence
  only**, never a current instruction (index: §15.4).
- The ledger does not define Driver meaning. **Each task's frozen packet owns the meaning.**
- For real work, still open the exact live code, the frozen task packet and the named result
  files. This document points at them; it does not replace them.
- Neither source authorizes a model run. *(Handoff: it "records how Qwen-specific test runners
  should call the shared local client. It does not authorize a model run.")*

---

## 3. Machines and server

### 3.1 Who owns what

| Machine | Role |
|---|---|
| **Minisforum** `<user>@<MINISFORUM_IP>` | Owns everything that is work: Codex, Core, the repository, all code, harnesses, documentation and results. Harness interpreter: `<REPO>/venv/bin/python`. Development happens first in a shadow copy of the repo (§10.2). |
| **Mac** | Serves Ollama inference and **nothing else**. Its scratch files are disposable. **No repository work happens on the Mac** (D11). |

Only these belong on the Mac:

- Ollama itself and its launchd plist `~/Library/LaunchAgents/com.<mac-user>.ollama.plist`;
- which model is resident, keep-alive and parallelism;
- the autossh reverse tunnel that exposes the Mac's Ollama as `localhost:11434` on the Minisforum.

### 3.2 Mac hardware

14-inch MacBook Pro, M4 Pro (12-core CPU, 16-core GPU), **48 GB**. It ships with a 70 W adapter
but was run on a 30 W charger; a 61 W adapter was attached later. The power effects are in §3.4.

### 3.3 Server environment — last recorded 2026-08-17 from the plist, not verified live

Every value below — plist contents, resident model, keep-alive, parallelism and the tunnel — is
**UNKNOWN until a read-only preflight confirms it**.

    OLLAMA_HOST=0.0.0.0:11434
    OLLAMA_NUM_PARALLEL=1
    OLLAMA_LOAD_TIMEOUT=30m
    OLLAMA_KEEP_ALIVE=-1
    OLLAMA_MAX_LOADED_MODELS=1

- Apply changes with `launchctl bootout` then `bootstrap`. `launchctl kickstart -k` does **not**
  reload environment variables.
- Restarting Ollama drops the whole prefix cache.
- Why `NUM_PARALLEL=1` and `LOAD_TIMEOUT=30m`: §13.3.

### 3.4 Conditions for a long batch run on the Mac (measured — they matter)

- **Keep other apps light.** With the model resident (about 19–29 GiB depending on context), the
  Mac swaps heavily when much else is open. Swap was 95% full on 2026-08-17 and reached 22.9 GiB
  during the 2026-08-18 capacity probe, which dropped prefill from the usual 95–110 tok/s to 83.
- **Sleep the display.** Display sleep had been disabled (`pmset displaysleep 0`), and the display
  stack was eating most of the adapter's power: charging rose from 142 mA to 1,781 mA after
  `pmset displaysleepnow`. Run `pmset displaysleepnow` before a long batch.
- **Gate on battery.** Under GPU load the battery drains about 2%/min even while plugged into the
  undersized adapter, and identical calls ran up to 3.5x slower once the battery fell to 5–16%.
  Batch jobs must be **resumable and battery-gated**, and every reported timing should carry a
  battery reading.

---

## 4. Models

### 4.1 Models — last recorded

| Model tag | Engine / quant | Status | What it is good for |
|---|---|---|---|
| `qwen3.8:27b-mlx` | MLX engine, nvfp4, dense 27.8B, arch `qwen3_5` | **Default** (`LOCAL_LLM_MODEL`) | The table suites (choice_v2, row_v3, qf01). Does **not** enforce a `format=` schema. Failed the identity judge (answered in prose) and the reader (returned nothing). |
| `qwen3.8:27b-mtp-q4_K_M` | GGUF Q4_K_M | Second model on the server | **Grammar-enforces** a `format` schema, at roughly **3x slower decode**. The only working mode for the identity judge and the reader exam (reasoning off). |
| `qwen3.6:35b-a3b` | GGUF Q4_K_M; MoE 36B total / 3B active; digest `07d35212591fc27746f0a317c975a6d68754fb38e9053d82e25f06057af28522`; Ollama 0.32.3 | **Removed 2026-08-15** | The original model and the handoff's default. The ledger says "both qwen3.6 tags" were removed that day without naming the second. The handoff had also named `qwen3.6:35b-mlx` (faster, no schema enforcement); the 2026-10-19 live check found no qwen3.6 tag installed. |

### 4.2 Rules

- **One model per run.** Only one model is resident at a time on the 48 GB machine. Switching is
  a **frozen-runtime change that needs its own record**. *(Handoff, measured on the old qwen3.6
  setup and not re-measured since: a switch costs about 8–14 s.)*
- A different GGUF or schema-enforced build, or reasoning turned on, is a **separate runtime**
  with its own qualification and frozen record — never a fallback reached from inside another
  runtime.
- **Do not casually upgrade Ollama.** 0.32.14 changes Qwen system-message handling; priming and
  every suite result would need re-verification.

---

## 5. The client: `config/local_llm.py`

### 5.1 Identity

The **only** local entry point. No other transport, wrapper, provider SDK or compatibility layer
may be introduced.

    path    config/local_llm.py
    sha256  836e5722ec01c5e1ef53b8eeb2675beb4fcb58d9e10b22570afc3c00daf80b66
    lines   388
    (hash verified 2026-08-20; re-verify before every run and record it)

- It contains no API key, no provider SDK and no external endpoint.
- `resolve_host()` tries `LOCAL_LLM_HOST`, then `http://<MAC_HOSTNAME>.local:11434`, then
  `http://<MAC_IP>:11434`, and raises `ConnectionError` if none answer. That is host resolution
  on the LAN, not provider substitution; there is no fallback arm.
- Its first docstring line is stale (D12).

### 5.2 Import and API *(handoff, corrected by the ledger)*

```python
import sys

sys.path.insert(0, "<REPO>")
from config import local_llm as L
```

| Call | What it does | In graded work? |
|---|---|---|
| `L.generate(prompt, system=None, max_tokens=4096)` | Free text → `str`, or `(str, stats)` with `with_stats=True`. | **Yes — the only one.** Use the full form in §6.1. |
| `L.structured(prompt, schema_dict, system=None)` | Structured output → `dict`, or `(dict, stats)` with `with_stats=True`. Schema enforced by grammar on GGUF only. | No (D2) |
| `L.reason(prompt)` | Reasoning on (slow). | No |
| `L.fast()` | Reasoning off (the default). | No |
| `L.health()` | Read-only check. Returns `{host, model, version, num_ctx, input_token_budget, loaded}`. | — |
| `L.prime(...)`, `L.prime_for(...)` | Cache priming (§8.1). | Optional transport step |
| `python -m config.local_llm` | **Not read-only** — makes a real model call (D5). | — |

**Exceptions.** Either one means the request failed structurally; it must **never** be treated as
a valid model answer.

| Exception | Meaning | Caveat |
|---|---|---|
| `L.TruncatedInputError` | The prompt exceeded the input budget, and its front would be lost. | **Never fires on MLX**; on GGUF it is detected from the response, after the call (§7.3). |
| `L.TruncatedOutputError` | Output reached the context limit when no `max_tokens` was supplied. | With `max_tokens` set it does not fire; check the stats flag instead (D7). |

### 5.3 Settings — resolve, freeze and record per run

Every value below can be changed by an environment variable read at import, or by the server
(D8). These are **last recorded, not live**.

| Identity | Comes from | Last recorded value |
|---|---|---|
| model (`L.MODEL`) | `LOCAL_LLM_MODEL` | `qwen3.8:27b-mlx` |
| host | `LOCAL_LLM_HOST` / mDNS / IP | resolved at call time |
| thinking default | `LOCAL_LLM_THINK` | `0` (off) |
| num_ctx default (`L.NUM_CTX`) | `LOCAL_LLM_NUM_CTX` | `32768` |
| timeout default | `LOCAL_LLM_TIMEOUT` | `1800` s |
| Ollama version | server | `0.32.13` |
| engine / quant | server | MLX engine, nvfp4, dense 27.8B, arch `qwen3_5` |

### 5.4 Stats returned with `with_stats=True`

`tok_s`, `eval_count`, `prompt_eval_count`, `done_reason`, `truncated_input`,
`truncated_output`, `total_s`, `host`.

They do **not** include the model id, `num_ctx`, `think` or `temperature`, so record the resolved
identity from §5.3 separately (D6).

---

## 6. Graded-call contract

### 6.1 The call

Use only `L.generate()`. Pass the frozen prompt and system text through unchanged, and pass
**every argument explicitly** — defaults are unsafe or environment-controlled.

```python
from config import local_llm as L

text, stats = L.generate(
    prompt,                    # the frozen packet prompt, byte-for-byte
    system=SYSTEM_TEXT,        # the frozen system text, or None if the packet has none
    think=False,               # explicit; the env default is not trustworthy
    temperature=0.0,           # explicit
    num_ctx=NUM_CTX,           # explicit, fixed for the entire run
    max_tokens=MAX_TOKENS,     # explicit, positive, fixed
    timeout=1800,              # explicit
    retries=0,                 # explicit; the default is 2 (D1)
    with_stats=True,
)
```

*(Handoff, old qwen3.6 setup, not re-checked since: temperature 0 was the default and produced
byte-identical, deterministic output in the supplied checks. Pass it explicitly anyway.)*

### 6.2 Forbidden in a graded call

- `structured()` — it rewrites the prompt, strips fences and retries (D2);
- `fast()` and `reason()` — extra wrappers, and `reason()` turns thinking on;
- `format=` — a schema-behaviour difference from the comparison arm, and MLX ignores it anyway;
- any added instruction, altered schema, shortened context or hidden answer in the input;
- any API call, alternate provider, fallback, cascade or vote;
- any automatic retry of a completed answer.

These bans describe the **current MLX / 196-item configuration**. Any other build or reasoning
setting is a separate runtime (§4.2).

### 6.3 One call at a time

The caller runs **strictly sequentially, `workers=1`**. The client does not enforce this (D9);
`OLLAMA_NUM_PARALLEL=1` on the server is a backstop, not a guarantee.

### 6.4 Handling the output

1. **Raw first.** Write the model's exact reply to its own file before any parsing, stripping,
   normalising or validation. On this path `L.generate()` returns the assistant text unmodified.
2. **One strict, shared parser.** The same parser, normalizer and validator the comparison arm
   uses: plain JSON, or a single whole-response fence. No provider-specific parser, no repair pass.
3. **A cut-off or incomplete output is invalid** once its raw form is saved. With `max_tokens`
   set, the client returns a cut answer without raising (D7), so the runner must check
   `stats["truncated_output"]` and `done_reason` itself and reject it.
4. **Never repair an answer.** Code may parse, validate, re-pull source spans and reject. It may
   never change the model's chosen row, meaning, name, route, type or concept.

### 6.5 Retries

- A transport failure with no usable response is not an answer.
- `L.generate(retries=0)` is **mandatory** — the library must never retry on its own.
- Separately, a frozen task **may** authorize a bounded **caller-level** retry for a transport
  failure or an invalid output. If it does, the bound is fixed before the run, every attempt is
  recorded, and a **completed answer is never re-asked**. Nothing retries silently.
- Library retries and caller attempts are counted separately (§16).

### 6.6 Accounting

Record every event, per item: the call, any prime, transport failures, refusals, invalid answers,
cut answers and every unserved input. Report correct, wrong, abstained, invalid and missed as
**raw counts, never as a rate alone**.

---

## 7. Capacity, pre-call safety and speed

### 7.1 Two numbers — do not conflate them

| Figure | Meaning |
|---|---|
| **25,000 tokens** | the **conservative safe operating limit** — use this |
| **29,492 tokens** | a **single stress success** — evidence only, not a ceiling (D10) |

- **The 29,492-token run (2026-08-18):** a 28,092-token prompt plus 1,400 generated tokens
  completed at `num_ctx=32768` — wall 404.2 s, prefill 83.1 tok/s, decode 21.3 tok/s. The Mac was
  swapping heavily at the time (§3.4), which is why prefill sat below the usual band. One success
  does not authorize routine calls at that size.
- **Memory:** runner memory grows roughly 0.24 MB per prompt token. 13.7k tokens peaked at
  33.9 GiB and 23.5k at 36.2 GiB, against a 37.4 GiB Metal budget on the 48 GB machine. A
  70k-token prompt would need about 47 GiB — impossible here.

### 7.2 `num_ctx` is fixed per role for the whole run

- **16384** for tables and chunks up to about 12k tokens; **32768** for whole exhibits (tested to
  23.5k tokens).
- Never change it mid-run or vary it by case: that reloads the model and drops the entire cache,
  so the next document is read cold. *(Handoff, old qwen3.6 setup, not re-measured: the reload
  alone took about 8 s.)*

### 7.3 Open blocker: no genuine pre-call token check

The current MLX client cannot refuse an oversize input before calling:

- `trunc_in = (not _is_mlx(MODEL)) and pec >= budget - 8` — `_is_mlx("qwen3.8:27b-mlx")` is
  `True`, so this is always `False`, and `TruncatedInputError` can never fire on the production
  model;
- even on the GGUF path the check reads `prompt_eval_count` **from the response**, so it detects
  truncation after the call, never before;
- there is no tokenizer and no length check anywhere in the client.

**A transport may never truncate or split a frozen input** to make it fit. An input that does not
fit is refused before the call and counted as unserved. A task owner may later design
self-contained chunks as a **separately qualified task**; the transport cannot invent them.

**Do not prescribe tokenizer machinery yet.** A later task must first measure the final frozen
prompts, then choose the smallest sufficient pre-call check. That decision is not made here.

### 7.4 Estimating time and size before you call

```
call time  ~=  new_prompt_tokens / 95  +  output_tokens / 25    (seconds)
```

- **Fresh, never-seen text:** 95–110 tok/s prefill — the GPU ceiling. Nothing makes a brand-new
  document faster except sending fewer tokens.
- **Cached prefix** (same bytes from position 0): effectively free, about 1 s per call.
- **Decode:** 22–29 tok/s with MTP speculative decoding on; 34.3 tok/s once on a freshly
  restarted, idle machine (2026-08-19). GGUF is roughly 3x slower.
- **Measured cold calls:** 6k-token table 65 s; 13.7k-token 8-K exhibit 145 s; 23.5k-token
  exhibit 261 s.
- **Rough token count before tokenizing:** numeric tables about **1.6 chars/token**, prose about
  **3.4 chars/token**. Every digit is its own token; indentation and separators are tokens too.
  This is a planning estimate, never a substitute for the pre-call check in §7.3.
- **Never send raw HTML** — the same exhibits cost 10–20x the tokens of the rendered text.

### 7.5 Sending fewer tokens is the only software lever

The encoding that produced 93/93 on the table lanes:

```
Source-derived choices. Every choice line is choice|occurrence|value|headers:   ← one header line
ROW n section="..." label="..."                                                ← per row
22|1|2,289|4Q24                                                                ← choice lines, no indent
<per-call target block>                                                        ← last
```

Code applies the occurrence; **the model never counts**. Dense encoding cut tokens 46% against
verbose prompts; dropping the indent and using a single `cols` legend cut a further 16.7%.
Reference implementation (historical): `qwen38_optimization/harness/choice_v2_compact/choice_v2.py`.

---

## 8. Caching and priming

**Layout rule: stable bytes first, the varying item last.** Ollama reuses a KV prefix only when
the bytes match from position 0. Any changing token placed early — an id, a date, a nonce —
destroys reuse for everything after it.

**The cache affects speed only.** It changes no prompt bytes and no answer. Priming is a transport
step.

### 8.1 Priming

Priming is **optional**, happens **only after the capacity checks pass**, and is **recorded**.

Why it exists: the MLX runner creates a branch-point snapshot only during the *second* request
that diverges there, and this model's recurrent layers cannot be rewound — so the first two calls
on a shared document would both be cold. Sending the shared prefix alone first leaves a snapshot
that the first real call restores from.

```python
L.prime(shared_prefix, system=SYSTEM_TEXT, num_ctx=NUM_CTX)   # once per document
L.prime_for(prompts, system=SYSTEM_TEXT, num_ctx=NUM_CTX)     # computes the prefix for you
```

Conditions: the same model, system text and `num_ctx` as the real calls; the prefix starts at the
beginning of the user content and ends on a line boundary. Priming an already-cached prefix costs
about 0.1 s.

**One document batch at a time; no parallel calls.** The cache holds roughly 8 GiB of snapshots,
and interleaving documents evicts them.

### 8.2 Which roles benefit (assessed 2026-08-17, not freshly measured)

| | Roles (of 7 real AI roles) |
|---|---|
| **Helped (3)** | reader (many items per event); table/prose locator (many anchors per table); concept picker (many facts per company menu). These are the high-volume roles, so by call count roughly 70–80% of calls could be cache-fast after each document's one cold read. |
| **Not helped (4)** | catalog chunk reader (each chunk read once); identity judge; continuity judge; graders/reviewers. Each reads its input once at the plain rate, but the inputs are small, so each call still costs only seconds. |

By step, caching was assessed to help **Steps 3, 5, 8, 9 and 11**.

Getting the benefit changes no question or answer: put the shared document **before** the per-call
part (a prompt-layout change, so re-freeze that prompt version) and add one `L.prime()` per
document.

**Measured effect** (evidence, not a promise): one 6.2k-token table, 3 calls, 155 s → 78 s with
identical answers; full choice_v2 9.0 → 5.3 min with compact encoding and table-level priming;
qf01 7.4 → 3.4 min.

---

## 9. Model-neutral qualification

- **One canonical semantic packet per task.** Every runtime gets the same semantic instructions,
  the same complete context and item order, the same input identities and the same response
  contract.
- **The same hidden key, parser, validator, scorer and pass bars** apply to Sonnet, Codex-hosted
  models and Qwen alike; only a thin transport differs. A transport may encode the packet but
  never shorten or change it.
- **The hidden key never enters a runtime input.** *(Handoff: hidden answers and task-specific
  scoring stay outside the model prompt.)*
- **Qualification does not transfer.** It belongs to the exact task, model and runtime, transport
  and configuration, and tested input class. It never transfers automatically to another task,
  another model or another input class.
- **The runtime that produced an answer never grades it.**
- **Zero observed wrong accepted results is mandatory.** Count every refusal, miss and unserved
  item.
- **Freeze before every run:** runtime, model, transport, configuration, reasoning setting,
  measured capacity and input class *(handoff adds: prompts, inputs, answer-key hashes and
  scorers)*. Drift, unsupported capacity or possible truncation must refuse **before** the call,
  not after.

"100%" means zero observed errors on a finite locked set; it does not prove a zero true error
rate. Report the independent-case count beside every zero-error claim — for the table suites that
is **8 tables from 7 filings**, not 93 documents.

---

## 10. Repository rules and workflow

### 10.1 Allowed repository paths

A Qwen change may touch **only**:

1. `config/local_llm.py`
2. `.claude/plans/Drivers/FinalDesign/QwenTests/qwen38_optimization/`
3. `.claude/plans/Drivers/FinalDesign/LeftOverSteps/QwenInference.md` (the ledger)

The owner's working tree carries unrelated modifications, so stage only the **exact,
independently reviewed, changed files** inside those three roots — by explicit path; never a whole
directory, `git add -A` or `git add .`. Staging, commit and push all require a later explicit
completion review (§10.2, step 5). The ledger was untracked before its migration and will be
tracked when landed.

### 10.2 Workflow

1. **Shadow first.** Make every change in the shadow tree `/tmp/qwen38_bench/EventMarketDB`, a copy
   of the repo; never edit the real tree to try something out. Verify the artifact the run actually
   reads — prompts baked into `cases.jsonl` at prepare time, and the shadow tree's own copy of the
   client, have both silently defeated edits before.
2. **Review independently.** Produce the exact diff, the tests and the evidence, and read them as a
   reviewer, not as the author.
3. **Apply only the accepted change** to the real Minisforum repository, by hand, file by file.
   Only reviewed code and its regressions ever run there — never exploratory work — and the whole
   shadow tree is never copied over the real one.
4. **Stage only the exact reviewed files** inside the allowed roots (§10.1), by explicit path.
5. **Staging, commit and push all wait for an explicit completion review** — never part of doing
   the work.

---

## 11. Known defects (D1–D12)

Live defects in the client or in earlier documentation. Other sections cite them by number.

| # | Defect | What to do |
|---|---|---|
| **D1** | `generate()` defaults to `retries: int = 2`, so a call that omits it may make up to three attempts. | Pass `retries=0` in graded work. |
| **D2** | `structured()` modifies the prompt: on MLX it appends `"Return JSON only - exactly one object matching the schema, no prose, no code fence."`, strips code fences from the reply, and retries up to three model calls. | Never use it for graded or compared work. |
| **D3** | MLX has no pre-call token guard — no tokenizer, no length check (§7.3). | Until a pre-call check exists, run no input near the capacity limit (§1). |
| **D4** | `TruncatedInputError` is not a working pre-call gate: disabled for MLX by construction, and evaluated from the response in any case (§7.3). | Treat any claim that the client refuses oversize input before the call as **false** — earlier versions of the ledger said exactly that. |
| **D5** | `python -m config.local_llm` is not a read-only health check; its `__main__` block makes a real model call. | Use `L.health()` or the HTTP endpoints. |
| **D6** | `with_stats=True` returns `host` but not the model id, `num_ctx`, `think` or `temperature`. | Record the resolved identity separately. |
| **D7** | An explicit `max_tokens` suppresses the output-truncation exception (the raise is guarded by `max_tokens is None`), so a cut answer comes back normally with `truncated_output=True`. | The runner must reject it. |
| **D8** | `LOCAL_LLM_HOST`, `LOCAL_LLM_MODEL`, `LOCAL_LLM_THINK`, `LOCAL_LLM_NUM_CTX` and `LOCAL_LLM_TIMEOUT` are read at import, so host, model and thinking defaults are environment-controlled. | Resolve and freeze them; never assume the documented default. |
| **D9** | The client has no lock or semaphore, so nothing enforces sequential calls. | The caller owns it (§6.3). |
| **D10** | The 29,492-token success is evidence, not a universal safe ceiling (§7.1). | Use 25,000. |
| **D11** | Mac-side repository commands are obsolete. Earlier recipes ran the identity and reader exams on the Mac against `localhost` and copied keys and the client next to the exam scripts there. | Do all repository work on the Minisforum. |
| **D12** | The client's docstring opens with "Local LLM client — Qwen3.6-35B served from the Mac over the LAN", while its own body correctly documents the 2026-08-15 migration to `qwen3.8:27b-mlx`. | No behavioural effect; ignore the first line. |

---

## 12. Results registry

### 12.1 Runs that happened

#### QF-01 original per-cell contract — FAILED

| Field | Value |
|---|---|
| Date | 2026-07-24 |
| Purpose | one anchor + one rendered table → complete evidence-ID set |
| Input class | rendered 8-K tables |
| Model | `qwen3.6:35b-a3b` GGUF Q4_K_M, digest `07d35212…`, Ollama 0.32.3 |
| Settings | reasoning off, temperature 0, no completed-answer retries, 4 concurrent workers |
| Key | opened after the run |
| Outcome | 93 calls · **correct 0, wrong 92, abstained 0, invalid 1** · precision 0%, recall 0% |
| Cost | 43 min 31 s · 1,004,082 input tokens · 17,114 output tokens · zero input truncations, one output truncation |
| Verdict | **`NOT_SAFE_FOR_TASK`** · report `table_evidence/REPORT.md` |

Every parseable answer missed the exact period-header array. **Diagnostic only. The 93 cases are
now development data and can never certify a tuned prompt.**

#### choice_v2 — development, opened key

`test_id QF-01-CHOICE-V2-DEV`. The model chooses a numbered cell or `null`; code reconstructs the
evidence. 93 cases from 8 independent tables in 7 filings, 93 calls. Settings: reasoning off,
temperature 0, `num_ctx` 16384, `max_tokens` 512, timeout 1800, workers 1, completed-answer
retries 0.

| run | model | correct | wrong | precision | artifact identity |
|---|---|---|---|---|---|
| old model | `qwen3.6:35b-a3b` | 75/93 | 18 | 0.806 | raw `5e7aa705…` |
| verbose prompts | `qwen3.8:27b-mlx` | 89/93 | 4 | 0.957 | raw `ef292ce3…` |
| dense + occurrence labels | `qwen3.8:27b-mlx` | **93/93** | 0 | **1.0** | raw `b5bf1f2b…` |
| + family priming, 9.0 min | `qwen3.8:27b-mlx` | 93/93 | 0 | 1.0 | raw `013278c9…` |
| + table priming, 6.4 min | `qwen3.8:27b-mlx` | 93/93 | 0 | 1.0 | raw `3faa3aa4…` |
| compact encoding, 5.3 min | `qwen3.8:27b-mlx` | 93/93 | 0 | 1.0 | raw `da73a80d…` |

Abstained 0 and invalid 0 in every row; transport failures 0 except the first 93/93 run (2). All
runs are marked `production_authorized: false`, `unseen_certification_required: true`. Every
qwen3.8 error before the dense + occurrence fix was `WRONG:occurrence`.

#### row_v3 — development, opened key

`test_id QF-01-ROW-V3-DEV`. The model selects a row only; code applies the explicit occurrence and
copies the evidence. 93 cases. `qwen3.8:27b-mlx` **93/93**, precision 1.0 (raw `5e6ae72f…`); the
old `qwen3.6:35b-a3b` also 93/93 (raw `8be8187e…`). The easiest task by construction. Needs no
priming — prompts within a family are identical.

#### qf01 aligned 5x50 contract — development, opened key

`test_id QF-01`. 19 set-based calls covering 93 hidden cells across 8 tables in 7 filings.
`qwen3.8:27b-mlx`: **correct 19, wrong 0, abstained 0, invalid 0**; evidence precision and recall
1.0. The scorer printed the **historical label** `QWEN_ONLY_QUALIFIED` — a string it emits, which
confers no authority. Scored 2026-08-17T05:13:24Z; 3.4 min with table-first priming (was 7.4 min).
Manifest `3bd50ef6…`, raw `cb725f4d…`, hidden key `b4a26aa5…`. Old model: 17/19.

The manifest records that the 2026-07-24 run authorization was consumed by the failed original
run, so **a new model run needs its own owner GO**.

#### Identity judge (EXP-0 contract, QC-01) — development, opened key

2026-08-17. K-pairs v1.3: 160 planted pairs (110 DIFFERENT, 50 SAME, 89 hard, 13 families).
Model **`qwen3.8:27b-mtp-q4_K_M`** (GGUF, schema grammar-enforced) — the MLX build answered in
prose and was invalid. 160 calls, one pair per call.

| Measure | Result |
|---|---|
| Counts | **correct 157, wrong-SAME 0, false refusal 2, invalid 1** |
| Rates | wrong-SAME 0.0 · false refusal 0.04 · invalid 0.0063 |
| Gate | `gate_pass: true` against wrong-SAME = 0, false refusal ≤ 10%, invalid ≤ 2% |
| Citations | verbatim on both sides 159/160 |
| Time | 4,541.6 s total, 28.39 s/pair |
| Baselines | Sonnet arm A 0/0/0 · Sonnet arm B 0 wrong-SAME / 1 false refusal / 0 invalid · Opus 0/0/0 |

All 3 non-perfect cases fell in the `synonym` family. The single invalid was a 600-token
output-cap artifact; re-asked at a 1,500-token cap it returned a valid DIFFERENT.

**Diagnostic only.** Even a perfect score would not activate Qwen as an identity judge; full
identity testing needs K-pairs v2 with mined real pairs.

#### Reader EXP-2 proxy — development, opened key, partial

2026-08-17. The first **10 of 40** chunks, 296 gold facts. `qwen3.8:27b-mtp-q4_K_M` in grammar
mode, reasoning off, `max_tokens` 8000. MLX returned nothing with reasoning off and ran away past
8–12k tokens with reasoning on, so grammar-enforced GGUF with reasoning off was the only working
mode.

| metric | Qwen | Sonnet | Opus |
|---|---|---|---|
| either-recall | **50.0%** (148/296) | 45.3% (134) | 52.4% (155) |
| exact-name recall | 32.8% (97) | 32.1% (95) | 35.5% (105) |
| hard-subset either | 39.8% (39/98) | 49.0% (48) | 48.0% (47) |
| quote verbatim | 145/148 (98.0%) | 120/120 (100%) | — |
| name well-formed | 148/148 | 120/120 | — |

- **Compliance** on Qwen's 148 candidates: output shape 100%, name syntax 100%, NAME-01 146/148,
  verbatim 145/148, 60–200-character quotes 109/148. 2 of the 10 chunks returned empty.
- **Slip pattern** from 10 reviewed failures (2026-08-17). Name *syntax* is never wrong. The slips:
  - (a) direction or measure words creeping into names — `minimum_wage_increase` should be
    `minimum_wage`; `headcount_growth` should be `headcount`;
  - (b) breaking the 60–200-character verbatim-quote rule, far more often too short than
    paraphrased — e.g. "unfavorable product cost mix" (28 chars);
  - (c) naming the effect or measure instead of the underlying cause —
    `foreign_currency_forward_contract_costs` should be `foreign_currency_forward_contract`;
    `judicial_deposit` should be `brazil_tax_litigation`.

  Code can check (a) and (b) mechanically; (c) is the genuine judgment gap — the same failure class
  predicted to cost Qwen points on any quote-locator task.
- **Not the official EXP-2 metric.** The official metric used Sonnet graders. This is strict
  deterministic matching, with the Sonnet and Opus arms re-scored the same way, so it is a relative
  comparison only. Precision was not measured.

### 12.2 Tasks with no Qwen run

From the readiness map. `READY KEY` means hidden answers exist; it never means a runner is
approved.

| ID | Task | Key status | Qwen |
|---|---|---|---|
| QF-02 | 8-K prose: find the exact sentence with the known Driver's number and period | NOT READY, 0/50 locked | not run |
| QF-03 | Prepared remarks: find the exact spoken update | NOT READY, 23 unaccepted candidates | not run |
| QF-04 | Transcript Q&A: find the exact answer | NOT READY, same 23 candidates | not run |
| QF-05 | Numberless claim: copy the exact sentence | NOT READY, 0/50 locked | not run |
| QF-06 | Abstain correctly when no unique evidence exists | NOT READY, no negative cases | not run |
| QC-00 | Name a known cause under NAME-01..19 | NOT READY, K-reader does not isolate naming | not run |
| QC-02 | Interpret DriverUpdate fields | K-fields **drafting**, no lock | not run; EXP-5 P6 arm withdrawn 2026-07-25 |
| QC-03 | Route ATTACH/ADOPT/CLAIM/CREATE/SKIP/UNSURE | NOT READY, K-route absent | not run |
| QC-04 | Classify metric/guidance/surprise/action | NOT READY, K-stamp absent | not run |
| QC-05 | Select one XBRL concept from a bounded menu | NOT READY for Qwen, no locked key | not run |
| QC-06 | Challenge a proposed identity/concept match | PARTIAL only | not run |
| QC-07 | Judge stock direction/force/confidence | NOT READY, no locked key | not authorized |
| QE-01 | Create, verify and grade hidden keys | frontier duty | **not currently qualified or authorized** for Qwen's own test |
| QA-01 | Discover new Drivers in unseen text | frontier duty | **not currently qualified or authorized** |

### 12.3 Answer keys

| Key | Status | Path |
|---|---|---|
| `K-pairs.v1.3` | **Locked** — 160 pairs, lock `023fb1ce…` | `.claude/plans/Drivers/experiments/keys/K-pairs/K-pairs.v1.3.jsonl` |
| `K-reader.v3` | **Locked** — 1,175 records over 39/40 chunks, sha `cf87a09a…`, locked 2026-07-10 | `.claude/plans/Drivers/experiments/keys/K-reader/K-reader.v3.jsonl` |
| `K-fields` | **No key yet** — being drafted; the 196-item packet belongs to this drafting | `keys/K-fields/` — drafting files only, no key or lock (contents listed in §1) |

Locked keys are **never opened outside a scorer process**. The remaining 30 K-reader chunks are
historical, unused material inside the existing locked key — **not authorized next work**.

### 12.4 Standing caveat on every result above

Every result in §12.1 came from a **development set whose answers were opened**. None is a hidden
qualification; under the current, unchanged production-shaped gate all of them are
**diagnostic**. A fresh unseen holdout is required before any Qwen role is approved.

---

## 13. History

### 13.1 The qwen3.6 era and the redesign

- **Model:** `qwen3.6:35b-a3b` (GGUF Q4_K_M, MoE 36B / 3B active, Ollama 0.32.3). The original
  QF-01 per-cell contract failed outright: 0/93, `NOT_SAFE_FOR_TASK` (§12.1).
- **Diagnosis — the interface was as guilty as the model.** Occurrence markers split source
  headers; the flattened table did not attach cells to full header paths; and the model was charged
  with retyping long identifiers that code could have built. The redesign moved all deterministic
  copying into code.
- **Redesign.** choice_v2 (the model returns a number, code reconstructs) reached 75/93 on the old
  model — better, still not safe. row_v3 (the model picks a row, code applies the occurrence)
  reached 93/93 on both models but is the easiest task by construction.

### 13.2 Migration to `qwen3.8:27b-mlx`, 2026-08-15

Dense 27.8B, nvfp4, MLX engine. The trade: roughly **4x slower decode** than the old MoE build, in
exchange for qf01-aligned 17/19 → 19/19 and choice_v2 75/93 → 89/93. Both qwen3.6 tags were
removed the same day.

### 13.3 Performance investigation, 2026-08-15/17

The puzzle: identical work took 745 ms on one call and 7 minutes on another. Root causes, in the
order found:

1. `OLLAMA_NUM_PARALLEL=4` split `num_ctx` into four slots, so a 7.5k-token prompt overflowed its
   own slot → set to 1;
2. the default `OLLAMA_LOAD_TIMEOUT` of 5m aborted any prefill over ~300 s → set to 30m;
3. the client's hardcoded 300 s timeout aborted real calls → now 1800 s;
4. a LAN path reaps connections idle for ~320 s, while the server completes and caches the work
   anyway.

### 13.4 How choice_v2 reached 93/93 in 5.3 minutes

- **Accuracy:** 75/93 (old model) → 89/93 (qwen3.8, verbose prompts) → **93/93** (dense encoding
  plus explicit occurrence labels). GGUF reproduced the same wrong answers as MLX, **proving the
  weakness was the model's, not the quantisation's**.
- **Speed** for a full run at 100%: 25.2 min (old model, 75/93) → 9.0 → 6.4 → **5.3 min**. The
  levers were the token cuts in §7.5 and prefix priming (§8.1), which removed the second cold
  prefill per document.

### 13.5 Engine bake-off

| Engine | Prefill | Decode |
|---|---|---|
| Ollama MLX | 84–110 tok/s cold | 22–29 tok/s with MTP speculative decoding |
| llama.cpp b10450 Metal | pp6144 81.57 tok/s | tg32 9.77–10.10 tok/s |
| mlx-lm 0.31.3 | 84–88 tok/s | no MTP |

Dense 27.8B prefill on the 16-core M4 Pro GPU is compute-bound at roughly 85 tok/s. **No faster
engine was found among the tested configurations.**

### 13.6 Disproved claims (recorded so nobody re-derives them)

| Claim | What was really measured |
|---|---|
| "A cold 7.5k prompt takes 400 s" | a ~28k-token overflow, not prefill |
| "Streaming turns 399 s into 1.0 s" | a cold prompt compared against a cached one |
| "qwen3.8 is 3x slower than qwen3.6" | decode only, on a 17-token prompt |
| "Prefill runs at 100–180 tok/s at the roofline" | a sweep whose cases shared a prefix |
| A 16-inch machine or a 140 W adapter | wrong — see §3.2 |
| A "network middlebox idle timeout" | blamed before the real ~320 s reset was understood (§13.3) |

The full chronological working, every measurement and every dead end:
`qwen38_optimization/notes/INVESTIGATION_LOG.md` (811 lines) — **historical evidence, not current
instruction.**

---

## 14. Retired advice — never follow

### 14.1 Rejected by the ledger

- **"Retry until success."** The `scripts/autoresume.sh` pattern was **transport** retry against a
  harness that never re-asks a completed answer. It is not permission to retry an answer.
- Any **"route to Sonnet on failure"** or other automatic fallback inside a runner.
- Any **semantic word list, regular expression or keyword gate** standing in for a meaning
  judgment.
- **Reasoning on for the reader** — it ran away past 8–12k tokens (§12.1). Reasoning stays off;
  turning it on would be a separate runtime needing its own qualification, never a fallback.
- **`format=` as a validity guarantee on MLX** — MLX does not enforce it.

### 14.2 The handoff's stale advice → the current rule

| The handoff (2026-07-24) said | Current rule |
|---|---|
| `L.MODEL` defaults to `qwen3.6:35b-a3b`; `LOCAL_LLM_MODEL=qwen3.6:35b-mlx` is the faster option without schema enforcement | The last recorded default is `qwen3.8:27b-mlx` (§5.3); the qwen3.6 tags were removed 2026-08-15 (§4.1) |
| The input budget is about 16,000 tokens (`num_ctx 32768 / 2`), roughly 55,000–60,000 characters; larger input raises `TruncatedInputError`; tell the owner the largest required case if the budget must be raised | The conservative safe limit is **25,000 tokens** (§7.1), and `TruncatedInputError` is no pre-call gate (§7.3) |
| Four workers may fill idle gaps, though they do not multiply throughput | **`workers=1`, strictly sequential** (§6.3) |
| Aggregate throughput is ~50 tok/s regardless of concurrency (GPU memory bandwidth is the limit); estimate wall-clock as total output tokens ÷ 50 | Estimate with `new_prompt_tokens/95 + output_tokens/25` seconds (§7.4) |
| Use `L.structured()` for structured output; the default GGUF path enforces the schema | `structured()` is forbidden in graded work (D2); GGUF is last recorded as the second, non-default model (§4.1) |
| Shared reference runner `config/run_qwen.py`: `cases.jsonl → results.jsonl`, resumable, supports `--workers`; its header records the full input/output contract and all nine transport constraints; verified with 2 of 3 demo cases completing and the oversized case failing loudly with `TruncatedInputError`; task runners may copy its pattern or call it directly | Still on disk (dated 2026-08-01) but **outside the current contract** |
| Before any Qwen test, run `python3 config/preflight.py` and expect 13 structural checks with exit code 0 | Still on disk (dated 2026-08-01) but **outside the current contract**. For a read-only check use `L.health()` or the HTTP endpoints (D5) |

---

## 15. Artifact index

### 15.1 Current — authoritative

| Artifact | Purpose | Path | Identity |
|---|---|---|---|
| The ledger | the only current Qwen document | `.claude/plans/Drivers/FinalDesign/LeftOverSteps/QwenInference.md` | untracked before migration; tracked when landed |
| Client | the only local entry point | `config/local_llm.py` | sha256 `836e5722…`, 388 lines |
| Server plist | Ollama launchd config (on the Mac) | `~/Library/LaunchAgents/com.<mac-user>.ollama.plist` | last recorded — verify before running; a copy is in `qwen38_optimization/server/` |
| Shadow tree | where development happens | `/tmp/qwen38_bench/EventMarketDB` | rebuilt as needed |

Answer keys and their locks: §12.3.

### 15.2 Current — evidence behind §12

All under `.claude/plans/Drivers/FinalDesign/QwenTests/qwen38_optimization/`:

| Group | Path | Status |
|---|---|---|
| choice_v2 harness + 6 result sets | `harness/choice_v2/`, `harness/choice_v2_compact/` | development evidence |
| row_v3 harness + 2 result sets | `harness/row_v3/` | development evidence |
| qf01 harness + 3 result sets | `harness/qf01/` | development evidence |
| Identity exam runner + results | `exams/identity_exam/` | development evidence |
| Reader exam runner + results | `exams/reader_exam/` | development evidence, 10 of 40 chunks |
| Engine bake-off | `bakeoff/llama_bench_b10450_pp6144.md` | measurement |
| Original client + diff | `client/` | reference |
| Experiment scripts, queues | `scripts/` | reference |

### 15.3 Re-running a historical suite (reference only — not authorized work)

- Work in the shadow tree with `<REPO>/venv/bin/python`.
- Copy the patched harness over the **shadow's own copy**; editing the real tree's copy has no
  effect on a run. Prompts are baked into `cases.jsonl` at `prepare` time, so a prompt edit needs a
  fresh `prepare`.
- **Table suites:** `prepare` → `run` → `score`, with
  `LOCAL_LLM_MODEL=qwen3.8:27b-mlx LOCAL_LLM_NUM_CTX=16384`. `run` is resumable after a transport
  failure.
- **Identity and reader exams:** run from `qwen38_optimization/exams/*/` with their key and input
  files copied or symlinked next to the script (see each `README.txt`), on the GGUF model
  `qwen3.8:27b-mtp-q4_K_M` (MLX fails both — §4.1).
- **Expected wall-clock:** choice_v2 about 5–6 min · row_v3 about 4 min · qf01 about 3.5 min ·
  identity about 28 s/pair · reader about 6.6 min/chunk.

### 15.4 Historical — non-authoritative, do not follow

Preserved as evidence; none may be treated as a current instruction. **Do not delete or rewrite
them.**

| Document | Lines | Why superseded |
|---|---|---|
| `QwenTests/qwen38_optimization/QWEN_INFERENCE_GUIDE.md` | 337 | the previous canonical guide; its §9 contains the false pre-call truncation claim (D4) |
| `QwenTests/README.md` | 299 | 2026-07-24 readiness map; its §4 task table is reproduced in §12.2 |
| `QwenTests/LOCAL_QWEN_HANDOFF.md` | 97 | 2026-07-24 connection note; stale model, budget and worker advice (§14.2) |
| `QwenTests/table_evidence/REPORT.md` | 91 | the 0/93 failure report; still the best account of why the original design failed |
| `QwenTests/table_evidence/choice_v2/REPORT.md` | 69 | the 75/93 old-model report |
| `QwenTests/table_evidence/row_v3/REPORT.md` | 36 | the old-model row_v3 report |
| `QwenTests/table_evidence/{choice_v2,row_v3}/README.md` | 34 / 32 | harness notes |
| `qwen38_optimization/notes/INVESTIGATION_LOG.md` | 811 | the full chronological working behind §13 |
| `qwen38_optimization/notes/RUNBOOK.md` | 117 | v2 recipe, superseded by §§5–8 |
| `qwen38_optimization/notes/RUNBOOK_v1.md` | 63 | v1 recipe |
| `qwen38_optimization/notes/HANDOFF.md` | 22 | state summary at 2026-08-17 |
| `qwen38_optimization/README.md` | 45 | folder guide |
| `qwen38_optimization/harness/*/README_original.md`, `REPORT_original.md` | 34/69/32/36 | pre-change copies |
| `config/run_qwen.py`, `config/preflight.py` | — | 2026-08-01 helpers, outside the current contract (§14.2) |

---

## 16. Update template

Every later Qwen task must update the ledger's **current status**, **task registry** and
**artifact index**, and append **one dated entry** in this form:

```
### <YYYY-MM-DD> — <task name>

Purpose        : <one sentence>
Input class    : <what kind of input, and how many items>
Packet         : <path> sha256 <hash>
Prompt         : <assembled-prompt hash or per-item hash file> sha256 <hash>
Model/runtime  : <model id> · Ollama <version> · <engine/quant> · host <resolved>
Config         : think=<> temperature=<> num_ctx=<> max_tokens=<> timeout=<> retries=<>
Calls          : <n> issued · <n> primes · <n> transport failures
Library retries: 0 (mandatory — L.generate(retries=0))
Caller attempts: bound <n> authorized by the packet · <n> used · <n> items affected
Raw artifacts  : <path> sha256 <hash>
Score artifact : <path> sha256 <hash>
Key status     : <locked/opened/none> <key path> sha256 <hash>
Outcome        : correct <n> · wrong <n> · abstained <n> · invalid <n> · cut <n>
                 · refused-before-call <n> · unserved <n> · total <n>
Measured       : precision <> · recall <> (only where lawfully measurable; else UNKNOWN)
Runtime        : <wall> · <battery reading if on the Mac>
Decision       : <diagnostic | qualified for this exact task+runtime | failed>
Blocker        : <what still stands in the way, or none>
Next action    : <the single next permitted step>
```

Rules for every entry:

- no number without an artifact behind it;
- anything unproven is written **UNKNOWN**, never inferred;
- a development set with opened answers is labelled diagnostic;
- a result never claims authority over any task, model or input class other than the exact one
  tested.
