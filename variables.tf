variable "image_tag" {
    description = "Tag of the image using which a docker container is created"
    type = string
    default = "24.12.30"
}

variable "docker_repo" {
    description = "The docker repository from which the docker image should be pulled"
    type = string
    default = "novelty"
}