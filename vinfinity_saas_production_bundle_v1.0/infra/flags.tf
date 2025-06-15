module "launchdarkly" {
  source  = "launchdarkly/terraform-provider-launchdarkly"
  token   = var.ld_token
}
