provider "snowflake" {
  account  = var.snow_account
  username = var.snow_user
  password = var.snow_pass
}

resource "snowflake_database" "vinfinity" {
  name = "VINFINITY"
}
