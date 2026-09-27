# Open vs Hidden Evaluation Suites

## OPEN_SUITE

The entire evaluation is public and reproducible by any third party.

| Element | Visibility |
|---|---|
| Dataset | public |
| Expected results | public or reproducible from a deterministic generator |
| Baselines | public |
| Runner | public |
| Metrics | public |

**Use when** the task can be fully reproduced and benchmark gaming is not a primary risk. Examples: speech-follow alignment, interview-evaluation consistency, website static-structure checks.

**Cost:** any participant can overfit to the public cases. Mitigation: publish a large, diverse, deterministic dataset; require baselines to be simple reference algorithms; refresh the dataset on a versioned cadence with a new seed.

## HIDDEN_SUITE

The protocol and metric definitions are public; the evaluation data and the final evaluation runner are controlled by the operator.

| Element | Visibility |
|---|---|
| Protocol | public |
| Metric definitions | public |
| Development subset | public |
| Evaluation data | hidden |
| Evaluation runner | controlled |
| Submissions | black-box adapter; source code not required |

**Use when** anti-overfitting, anti-gaming, or adversarial evaluation is a primary requirement. Examples: quant strategy evaluation, future security/adversarial benchmarks.

**Cost:** the operator bears the reproducibility burden for the hidden set; public users cannot independently reproduce the final evaluation. Mitigation: the operator runs internal CI on the hidden set; the public dev set is fully reproducible; aggregate failure categories (not per-case hidden output) are reported back.

## Choosing a mode

- If a participant can trivially memorize the answers and that would invalidate the comparison, use `HIDDEN_SUITE`.
- If the value is in the diversity and determinism of the cases, not in their secrecy, use `OPEN_SUITE`.
- A benchmark may start as `OPEN_SUITE` and reserve a `HIDDEN_HOLDOUT` for later, to avoid evaluator tuning against public cases. The holdout is not used until it is frozen and the operator's evaluation pipeline is ready.
