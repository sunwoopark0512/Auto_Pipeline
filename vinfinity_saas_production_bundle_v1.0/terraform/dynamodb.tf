resource "aws_dynamodb_table" "feast_online" {
  name         = "feast-vinfinity"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "entity_id"
  attribute {
    name = "entity_id"
    type = "S"
  }
}
