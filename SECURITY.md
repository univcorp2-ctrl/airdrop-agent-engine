# Security

## Hard controls

v1 has no live submission method. `PublicGetClient` exposes HTTPS GET/fetch only, every adapter `execute()` hard-fails, and LIVE remains blocked even if all environment gates are manually set. Default live-capital/notional/loss/fee limits are zero.

Never store private keys, seed phrases, API secrets, cookies, bearer tokens, wallet signatures or withdrawal-enabled credentials in Git, chat logs, Notion, artifacts or CI output. Prefer scoped/subaccount/trading-only credentials with withdrawal disabled, session keys and IP allowlists where officially supported.

## Human Gates

Initial deposit, withdrawal, bridge, new contract approval, unknown wallet signature, signer add/change, leverage/capital/loss-limit increase and withdrawal-enabled API keys require direct human action. The agent must not bypass these gates.

## Prohibited behavior

Sybil farming, multi-wallet identity impersonation, KYC deception, self/wash/circular trading, fake liquidity, market manipulation, quote stuffing, self-referral abuse, anti-Sybil/bot detection evasion and VPN/proxy/fingerprint rotation to evade restrictions are prohibited.

## Kill switch

Stop on three consecutive API errors, stale data, paused/ended program, material Terms change, contract/address change, fee/loss/leverage cap breach, worsened legal status or loss/ambiguity of reward eligibility.
