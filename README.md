# Verdikt AI Prediction Market — GenLayer Intelligent Contract

A prediction market where GenLayer's leader/validator consensus reads
real web evidence and settles the market outcome — grounded in a
verifiable source, not a claim typed in by whoever calls the contract.

## Project Summary

Traditional prediction markets settle outcomes through manual
oracles, centralized admins, or rigid keyword-matching. This project
lets GenLayer's AI validator set fetch a news source itself and judge
whether it answers the market's question — settling YES / NO / NEEDS
MORE EVIDENCE on-chain, with every validator independently verifying
the same evidence before consensus is reached.

## Why GenLayer

- **AI judgement is the core value**: interpreting whether a
  real-world news article confirms or denies a plain-language
  prediction is exactly the kind of nuanced, natural-language task a
  deterministic smart contract cannot perform.
- **Web-aware decisions**: the contract fetches the evidence page
  itself inside the non-deterministic execution flow, rather than
  trusting arbitrary text supplied by the caller.
- **Consensus, not a single model call**: the leader's evaluation is
  independently re-derived by validators, who only need to agree on
  the settlement decision — not the exact wording of the reasoning.

## Live Demo

[https://isnoop4.github.io](https://isnoop4.github.io)

## Contract Details

| Field | Value |
|---|---|
| Network | [NETWORK — studionet] |
| Contract address | [0xE7319C622Dd50AFDB7D8D01b78f06e61bf989b26] |
| Explorer link | [https://explorer-studio.genlayer.com/address/0xE7319C622Dd50AFDB7D8D01b78f06e61bf989b26] |

## Tech Stack

- **GenLayer Intelligent Contract** — Python contract (`AIPredictionMarket.py`)
- **Frontend** — single-file static HTML/JS (`index.html`), calling the
  contract directly through the `genlayer-js` SDK, hosted on GitHub
  Pages (no build step)
- **Backend/database** — none; the contract is the sole source of
  truth for the question, resolution status, and verdict

## How It Works

1. **Deploy** — Contract is deployed with a plain-language market
   question (e.g. *"Will bitcoin reach $100,000 by end of year
   2026?"*).
2. **Resolve** — Anyone can call `resolve_market(source_url)` with a
   link to a news source. This triggers the leader/validator
   consensus flow:
   - The **leader** fetches `source_url` itself (`gl.nondet.web.render`)
     and asks an LLM to judge the market question strictly against
     that fetched content.
   - Each **validator** independently fetches the same URL and
     independently queries the model, then compares only the
     `verdict` field against the leader's result — not the wording of
     the reasoning, since independent LLM calls may phrase things
     differently even when they agree on the outcome.
3. **Settle** — Once consensus is reached, the verdict (`YES` / `NO` /
   `NEEDS_MORE_EVIDENCE`) is written on-chain along with a confidence
   level and a short explanation citing the evidence. The market is
   marked resolved and cannot be resolved again.

### Verdict JSON schema

```json
{
  "verdict": "YES" | "NO" | "NEEDS_MORE_EVIDENCE",
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "reason": "brief explanation citing the evidence"
}
```

### Contract methods

**Write**
- `resolve_market(source_url: str)` — fetches the given URL as
  evidence and settles the market; callable once, by anyone

**Read**
- `get_question()` — the market question
- `get_is_resolved()` — whether the market has been settled
- `get_verdict()` — the verdict JSON (`PENDING` until resolved)

## How to Run Locally

```bash
# 1. Clone the repo
git clone [https://github.com/isnoop4/genlayer-prediction-market]
cd [genlayer-prediction-market]

# 2. Open GenLayer Studio and load AIPredictionMarket.py
# 3. Deploy the contract with a constructor arg:
#    question: <plain-language market question>

# 4. Call resolve_market from any account, passing a source_url

# 5. Check get_verdict / get_is_resolved to see the result
```

### Running the frontend

`index.html` requires no build step. Two values must be set near the
bottom of the file before use:

```js
const CONTRACT_ADDRESS = "<0xE88Afe0fa00d8ab2156Aec593947D42558334AF0>";
const NETWORK = "studionet"; // or "testnetAsimov" once on public testnet
```

Then either open the file directly in a browser, or serve it locally:

```bash
python -m http.server
```

To deploy on GitHub Pages: place `index.html` at the repo root (or in
a `docs/` folder), then enable Pages in the repo settings pointing at
that branch/folder.

## Demo Evidence

Sample data to test quickly:

- **Question**: `Will bitcoin reach $100,000 by end of year 2026?`
- **Ambiguous source (produces NEEDS_MORE_EVIDENCE)**: a speculative
  price-prediction article that discusses possible future targets
  without confirming an actual outcome.
- **Clear source (produces a confident YES/NO)**: a dated news
  article that states Bitcoin's actual trading price plainly — the
  more directly a source answers the question, the more consistently
  validators agree.

## Known Limitations

- Resolution quality depends on how directly the supplied source
  answers the market question; ambiguous sources can lead to
  `NEEDS_MORE_EVIDENCE` or, on genuinely unclear evidence, more
  leader-rotation rounds before consensus is reached.
- If the source page's content changes between the leader's and a
  validator's fetch (e.g. live-updating price widgets, rotating ads),
  validators may disagree even on a question with a real answer —
  static news articles are more reliable evidence sources than live
  dashboards.
- `resolve_market` currently has no caller restriction — any address
  can trigger resolution once, using any URL they choose. This is an
  intentional "anyone can resolve" oracle-style design; it does not
  restrict resolution to the deployer.
- Each contract instance handles exactly one market question. A new
  market requires deploying a new instance.
- No dispute/appeal mechanism if a resolution is considered incorrect
  after the fact — resolution is final once consensus is reached.

## Future Roadmap

- Optional caller allowlist for who may trigger `resolve_market`
- Multi-source resolution (require agreement across more than one
  URL) for higher-stakes markets
- Factory contract to support multiple concurrent markets without
  redeploying
- On-chain staking/betting logic on top of the resolved verdict

## Security Notes

- All state changes (`verdict_json`, `is_resolved`) occur strictly in
  the deterministic write path, **after** the leader/validator
  non-deterministic consensus completes — no writes are reachable
  from inside the AI evaluation itself.
- The model's response is parsed strictly against an expected JSON
  schema; malformed or out-of-range values (e.g. a verdict outside
  `YES`/`NO`/`NEEDS_MORE_EVIDENCE`) raise an error rather than being
  silently accepted.
- Evidence is fetched by the contract itself from a caller-supplied
  URL, not accepted as free-form text — this prevents a caller from
  fabricating "evidence" to manipulate the outcome directly, though
  it does mean resolution quality still depends on which URL is
  supplied.
- The wallet-facing frontend never handles a private key; signing is
  delegated to the user's browser wallet extension.

---

*Built with GenLayer Intelligent Contracts.*
