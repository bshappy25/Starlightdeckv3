# Starplace Tomorrow Patch

Goal: A-soft gate + global confirm + strong theme takeover.

1) Add session key:
- global_confirmed default False

2) Add helper funcs:
- _confirm_everyone()
- _clear_confirmation()
- _is_confirmed()

3) Intake confirm button:
- call _confirm_everyone()

4) Theme takeover CSS:
- inject after profile load when confirmed

5) Reset user:
- call _clear_confirmation()