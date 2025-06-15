terraform {
  required_providers {
    render = {
      source = "renderinc/render"
      version = "~> 0.6"
    }
  }
}

provider "render" {
  api_key = var.render_api_key
}

resource "render_service" "api" {
  name           = "vinfinity-api"
  type           = "web_service"
  repo           = "https://github.com/your/repo.git"
  branch         = "main"
  env            = "docker"
  region         = "oregon"
  plan           = "standard"
  docker_context = "./"
  env_vars = {
    NOTION_API_SECRET = var.notion_key
    SUPABASE_URL      = var.supabase_url
  }
}
