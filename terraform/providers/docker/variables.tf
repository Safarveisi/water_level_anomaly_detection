variable "image_tag" {
    description = "Tag of the image using which a docker container is created"
    type = string
    default = "0.1.0"
}

variable "docker_repo" {
    description = "The docker repository from which the docker image should be pulled"
    type = string
    default = "novelty"
}