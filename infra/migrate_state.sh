#!/usr/bin/env bash
set -euo pipefail
TF_STATE="tfstate.json"
pulumi stack init dev || true

# 1) terraform state export
terraform show -json > $TF_STATE

# 2) import to pulumi
pulumi import --file $TF_STATE
pulumi state copy --from terraform
echo "✅  Terraform state migrated to Pulumi."
