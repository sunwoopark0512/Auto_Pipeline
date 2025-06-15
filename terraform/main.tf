provider "aws" {
  region = "us-west-2"
}
provider "google" {
  region = "us-central1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-bucket-name"
}

resource "google_compute_instance" "my_instance" {
  name         = "instance-name"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"
}
