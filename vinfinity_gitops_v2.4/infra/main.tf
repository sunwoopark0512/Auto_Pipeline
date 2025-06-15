terraform {
  required_version = ">= 1.6"
  required_providers {
    render = { source = "renderinc/render" version = "~> 0.6" }
  }
  cloud {
    organization = "vinfinity-lab"
    workspaces { name = "prod" }
  }
}

provider "render" {
  api_key = var.render_api_key
}

resource "render_service" "api" {
  name           = "vinfinity-api"
  type           = "web_service"
  repo           = var.github_repo
  branch         = "main"
  env            = "docker"
  region         = var.render_region
  plan           = "standard"
  env_vars = {
    NOTION_API_SECRET = var.notion_key
    SUPABASE_URL      = var.supabase_url
    SUPABASE_KEY      = var.supabase_key
  }
}
