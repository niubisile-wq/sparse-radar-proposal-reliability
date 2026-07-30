# Fair Ablation Hard Blocker Matrix

Date: 2026-07-28

This note records the exact residual rows that are still incomplete after the
latest closure pass, together with the current evidence status for each row.

## 1. Current residual set

The CSV currently has 0 incomplete rows.

## 2. Exact evidence status

| Row | Exact checkpoint / result path | Exact `log_eval` path | Current judgment |
|---|---|---|---|
| none | none | none | none |

## 3. Closest sibling artifacts found

These are not exact matches for the residual rows, but they are the nearest
related artifacts currently present on the instance:

- `msbc3 / astyx / 2028` has a usable `screen_q55msbc3` result and `log_eval`
  with AP `32.7835`
- `bevgate / kradar / 3407` now has a usable exact `result.pkl` and
  `log_eval` with AP `39.3228`
- `bevgate_dapg_msbc / kradar / 2028` now has a usable exact `result.pkl`
  and `log_eval` with AP `48.7151`
- `stable_bevgate_dapg_msbc / kradar / 2029` now has a usable exact
  `result.pkl` and `log_eval` with AP `52.5104`
## 4. Practical conclusion

There are no residual rows left in the CSV.
