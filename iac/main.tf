terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host = "http://localhost:2376"
}

resource "docker_image" "prefect" {
  name         = "prefecthq/prefect"
  keep_locally = false
}

resource "docker_container" "prefect" {
  image = docker_image.prefect.image_id
  name  = "tutorial"
  ports {
    internal = 4200
    external = 4200
  }
}
