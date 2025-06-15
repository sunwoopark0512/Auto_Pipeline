# v-Infinity Codex Admin Automation Module v1.1

## \ud83d\udce6 \uc8fc\uc694 \uae30\ub2a5
- Notion \uc6b4\uc601 \ub85c\uae45 \uc790\ub3d9 \ub4f1\ub85d
- CLI \ud30c\ub77c\ubbf8\ud130 \uae30\ubc18 \ub85c\uae45 \uae30\ub85d
- \ubc30\ud3ec \uc790\ub3d9 \ub85c\uae45 \uae30\ub85d
- Slack \uc7a5\uc560/\ub9c1\ub9ac\uc2a4 \uc2e4\uc2dc\uac04 \uc54c\ub9bc

## \u2699\ufe0f \uc124\uce58 \ubc0f \uc2e4\ud589
1. `.env` \ud30c\uc77c \uc0dd\uc131 \ubc0f \ud658\uacbd\ubcc0\uc218 \uc124\uc815
2. Notion DB \uc0ac\uc804 \uc0dd\uc131 (v-Infinity Ops Board \uc2a4\ud0a4\ub9c8 \uae30\ubc18)

## \ud83d\ude80 CLI \uc2e4\ud589 \uc608\uc2dc
```bash
python log_ops.py \
  --log_type "DevOps" \
  --operator "Sunwoo" \
  --module "ExportScript" \
  --environment "Local" \
  --task_summary "Full Export \ud14c\uc2a4\ud2b8" \
  --action_details "\ud3f4\ub354 \uc0dd\uc131 \ubc0f \uac80\uc99d \uc644\ub8cc"
```

## \ud83d\ude80 \ubc30\ud3ec \uc2a4\ud06c\ub9bd\ud2b8 \uc790\ub3d9\ub85c\uae45 \uc608\uc2dc
```python
from batch_log import auto_deployment_log

auto_deployment_log("Backend API", "Production", "v1.2.3")
```
