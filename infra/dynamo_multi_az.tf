resource "aws_dynamodb_table" "feast_online" {
  name         = "feast-vinfinity"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "entity_id"
  attribute { name="entity_id" type="S" }

  point_in_time_recovery { enabled=true }
  replica {
    region_name = "us-west-2"
  }
}

resource "aws_dax_cluster" "feast_dax" {
  cluster_name = "feast-dax"
  iam_role_arn = aws_iam_role.dax.arn
  node_type    = "dax.r5.large"
  replication_factor = 3
}
