# Sidekick

## Interpretation

The positioning map uses two axes to evaluate various AI voice assistants: one horizontal from "User-Friendly" on the left to "Secure" on the right, and another vertical from "Cost-Effective" at the bottom to "Privacy-Centric" at the top. The reference 'Sidekick' leads in both dimensions, indicating it excels in being user-friendly while also being secure and privacy-conscious. Among the most innovative assistants are Cresta Assist, which stands out for its forward-thinking approach despite not leading overall. Whisper/ LangChain is highlighted as particularly trustworthy due to its emphasis on privacy. The leaderboard combines scores from all axes: Sidekick maintains a strong position at the top-right, followed closely by pyannote OSS + Ollama and Diabolocom / Zaion. Allo-Media, Google Assist, LiveKit Agents, pipecat, and Kwak.ai also form an innovative cluster in the lower right quadrant, showcasing their focus on user-friendliness and cost-effectiveness while still maintaining a secure environment for users.

## Axes

- **Horizontal — User-Friendly ↔ Secure** (41% of variance). Columns by weight: TCO (+0.58) · On-prem privacy (+0.48) · Domain fit (FR, EV, closed routing) (+0.32) · Real-time streaming (+0.26) · Anonymization (PII+GDPR) (+0.21) · Speaker diarization / roles (+0.07) · Operator UX (-0.47).
- **Vertical — Cost-Effective ↔ Privacy-Centric** (22% of variance). Columns by weight: Anonymization (PII+GDPR) (+0.61) · Speaker diarization / roles (+0.49) · Operator UX (+0.46) · Domain fit (FR, EV, closed routing) (+0.39) · Real-time streaming (+0.09) · On-prem privacy (-0.07) · TCO (-0.11).
- Together the two axes retain **63%** of the total variation; the reference was rotated +15.3° to reach the top-right.

## Highlighted approaches

- **Leader (reference):** Sidekick
- **Weakest overall:** Zendesk AI Voice (lowest projection on the leader axis)
- **Most innovative:** Cresta Assist (frontier-capability projection)
- **Most trustworthy:** Whisper / LangChain (privacy / compliance projection)

## Leaderboard (by combined axis score)

1. Sidekick  (+2.98, +2.34)
2. pyannote OSS + Ollama  (+2.98, +0.41)
3. Diabolocom / Zaion  (+1.07, +1.87)
4. Allo-Media  (+0.70, +1.74)
5. Google Assist  (-0.04, +2.34)
6. LiveKit Agents  (+2.45, -0.17)
7. pipecat  (+2.45, -0.17)
8. Kwak.ai  (+0.81, +1.12)
9. Whisper / LangChain  (+2.38, -0.93)
10. Amazon Connect  (-0.11, +1.44)
11. Rasa Pro CALM  (+1.63, -0.51)
12. Azure Com + OpenAI  (+0.37, +0.28)
13. pyannoteAI  (+0.94, -0.46)
14. Cresta Assist  (-0.78, +1.08)
15. Talkdesk Copilot  (-0.59, +0.76)
16. Genesys AI  (-0.96, +1.13)
17. Gladia  (+0.85, -0.71)
18. Observe.AI  (-0.95, +0.80)
19. Vocode  (+1.37, -1.57)
20. Dialpad AI Contact  (-0.27, -0.10)
21. Open Granola  (+1.02, -1.40)
22. OpenAI Realtime  (+0.40, -1.23)
23. Anthropic Claude  (+0.40, -1.23)
24. OpenOats  (+1.32, -2.34)
25. NICE Enlighten AI  (-1.39, +0.10)
26. Aircall AI  (-0.71, -0.81)
27. Level (QA + real-time)  (-1.28, -0.52)
28. Cogito Coach  (-2.24, -0.04)
29. ASAPP GenAgent  (-2.24, -0.04)
30. Five9 AI  (-1.65, -0.65)
31. Salesforce Voice  (-2.98, -0.12)
32. Zendesk AI Voice  (-2.48, -0.80)

*Coordinates are PCA units; see the companion YAML for full coefficients.*
