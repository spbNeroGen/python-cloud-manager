variable "token" {
  type        = string
  description = "OAuth-token; https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token"
}

variable "cloud_id" {
  type        = string
  description = "https://cloud.yandex.ru/docs/resource-manager/operations/cloud/get-id"
}

variable "folder_id" {
  type        = string
  description = "https://cloud.yandex.ru/docs/resource-manager/operations/folder/get-id"
}

variable "default_zone" {
  type        = string
  default     = "ru-central1-a"
  description = "https://cloud.yandex.ru/docs/overview/concepts/geo-scope"
}

#---------------------------------

variable "instance_name" {
  type        = string
  description = "Имя виртуальной машины"
  default     = "simple-vm"
}

variable "instance_count" {
  type        = number
  default     = 1
}

variable "instance_cores" {
  type        = number
  default     = 2
  description = "Количество ядер для ВМ"
}

variable "instance_memory" {
  type        = number
  default     = 4
  description = "Объем памяти для ВМ в ГБ"
}

variable "instance_core_fraction" {
  type        = number
  default     = 100
  description = "Гарантированная доля vCPU"
}

variable "instance_disk_size" {
  type        = number
  default     = 30
  description = "Размер диска для ВМ в ГБ"
}