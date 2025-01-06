variable "image_tag" {
    description = "Tag of the image using which a docker container is created"
    type = string
    default = "25.01.06"
}

variable "docker_repo" {
    description = "The docker repository from which the docker image should be pulled"
    type = string
    default = "novelty"
}