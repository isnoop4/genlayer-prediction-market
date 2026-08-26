# GenLayer AI Prediction Market

## Project Summary
An Intelligent Contract-powered prediction market that uses GenLayer's GenVM LLM consensus to evaluate real-world news evidence and resolve market outcomes into structured JSON verdicts.

## Contract Details
- **Network**: GenLayer Studionet / Testnet Bradbury
- **Contract Address**: 0xF2803EB169D0eCb6286e787A05Aed2918A8D804e
- **Explorer**: https://explorer-studio.genlayer.com/address/0xF2803EB169D0eCb6286e787A05Aed2918A8D804e

## How it Works
1. Contract stores a prediction question.
2. User submits unstructured news summary evidence via `resolve_market()`.
3. GenLayer validators execute `exec_prompt()` to reach consensus on a structured JSON verdict (`YES`, `NO`, `NEEDS_MORE_EVIDENCE`).
4. Outcome state is saved on-chain.

## Live Demo
https://isnoop4.github.io/genlayer-prediction-market/
