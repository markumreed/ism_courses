# Week 12 design probes (2026-10-16)

Throwaway scripts run on the GPU while Week 12 was being designed, with
`granite4.1:3b` and an early version of the tools. They are the evidence for
the decisions table in the implementation plan, not page material; the pages
quote the CPU runs one folder up.

- `history_without_request_echo.txt`: tool results stored without the model's
  own tool request. 6 of 17 tool-using runs asked for the same lookup twice;
  one used up all three rounds. The vague address request led the model to
  invent order A100 and "123 Main St, Anytown" in 2 of 3 runs.
- `history_with_request_echo.txt`: the same, with the request stored. No repeated
  lookups in 16 tool-using runs; the invented address appeared in 1 of 3.
- `customer_said_first_draft.txt`: the first draft of the customer-said check.
  Every invented order ID or address was refused (6 of 6) and the model asked the
  customer, but run 4 of the three-turn case sent `new_address: ""`, which passed
  because an empty string is inside every string. The blank check now runs first.
