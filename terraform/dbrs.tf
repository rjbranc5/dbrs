provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
}

resource "aws_instance" "robert_brancale" {
  ami           = "ami-0ff8a91507f77f867"
  instance_type = "m5.large"
  key_name = "dbrs_key"
}
