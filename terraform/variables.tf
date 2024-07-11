variable "project_id" {
  type = string
  description = "Your Google Cloud project ID"
}

variable "region" {
  type = string
  description = "Region where the worloads run"
}

variable "service_name" {
  type = string
  description = "Your Cloud Run service name"
}

variable "db_instance_name" {
  type = string
  description = "AlloyDB Instance name"
  default = "ai-agent-db"
}

variable "db_user" {
  type = string
  description = "AlloyDB username"
}

variable "db_password" {
  type = string
  description = "AlloyDB password"
}

variable "db_database" {
  type = string
  description = "AlloyDB database name"
}
