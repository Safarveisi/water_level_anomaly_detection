terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_image" "app_image" {
  name         = "ciaa/${var.docker_repo}:${var.image_tag}"
  keep_locally = true
}

resource "docker_container" "app_container" {
  image = docker_image.app_image.image_id
  name  = "terraform-docker"

  ports {
    internal = 8501
    external = 8502
  }
}
