# Claims ledger

This ledger prevents the demo from outrunning its evidence.

| Claim | Status | Evidence | Limit |
|---|---|---|---|
| The legacy suite passes | Verified | `57 passed`; 48 parameterized legacy cases | Synthetic suite |
| Known-bad creates two captures | Verified | `run_scenario("known_bad")` | Deterministic simulator |
| Corrected behavior creates one capture | Verified | `run_scenario("corrected")` | Deterministic simulator |
| Held-out variant is blocked | Verified | `run_scenario("held_out_variant")` | One designed variant |
| Safe related change passes | Verified | `run_scenario("safe_change")` | One designed safety case |
| Gemini 3.5 Flash executes the agent team | Verified | Real Vertex run; three ADK terminal outputs | Project/model access dependent |
| ADK orchestrates three specialists | Verified | `SequentialAgent`, structured session outputs, trace | Sequential, not concurrent |
| Runs persist durably | Verified | Public run `run_5cb7da6518` in Firestore Native | Demo-scale schema |
| Incidents can enter asynchronously | Verified | Pub/Sub message `20705345734130924` created run `run_d672acdd75` | Demo trigger, not production event contract |
| Public cloud path works end to end | Verified | Hosting → Cloud Run → ADK/Gemini → evaluator → Firestore | Demo-scale deployment |
| GroundTruth prevents this class globally | **Not claimed** | Five-case demo matrix only | Requires broader domain evals |
| GroundTruth proves business ROI | **Not claimed** | Product thesis only | Requires longitudinal deployment data |

## Synthetic disclosure

All company, customer, payment-provider, order, code-change, and incident data are synthetic.
The order ID is not a real customer identifier. No payment network is contacted.
