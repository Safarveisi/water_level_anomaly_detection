terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_image" "novelty" {
  name         = "ciaa/novelty:24.12.30"
  keep_locally = false
}

resource "docker_container" "novelty" {
  image = docker_image.novelty.image_id
  name  = "terraform-docker"

  ports {
    internal = 8501
    external = 8502
  }
}
