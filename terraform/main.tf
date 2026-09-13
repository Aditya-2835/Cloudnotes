terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "cloudnotes_sg" {
  name        = "cloudnotes-sg"
  description = "Allow SSH and app traffic for CloudNotes"

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "CloudNotes app access"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "cloudnotes_server" {
  ami                    = "ami-05a3e9423ae4d7a19"
  instance_type          = "t2.micro"
  key_name               = "cloudnotes-key"
  vpc_security_group_ids = [aws_security_group.cloudnotes_sg.id]

  tags = {
    Name = "cloudnotes-server"
  }
}

output "public_ip" {
  value = aws_instance.cloudnotes_server.public_ip
}
