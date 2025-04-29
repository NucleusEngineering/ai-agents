terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 4.52"
    }
    google-beta = {
      source = "hashicorp/google-beta"
      version = "~> 5.30"
    }    
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = ["allUsers"]
  }
}

# Artifact Registry Repository
resource "google_artifact_registry_repository" "repository" {
  provider      = google-beta
  location      = var.region
  repository_id = var.service_name
  format        = "DOCKER"
}

# Cloud Run Service
resource "google_cloud_run_v2_service" "demo_service" {
  name     = var.service_name
  location = var.region
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello"
        env {
            name  = "PROJECT_ID"
            value = var.project_id
        }
        env {
            name  = "REGION"
            value = var.region
        }   
        env {
            name  = "FIRESTORE_DATABASE"
            value = var.firestore_database
        }
        env {
            name  = "DB_PASSWORD"
            value = var.db_password
        }
        env {
            name  = "DB_USER"
            value = var.db_user
        }
        env {
            name  = "DB_HOST"
            value = google_alloydb_instance.db.ip_address
        }
        env {
            name  = "DB_DATABASE"
            value = var.db_database
        }
    }
    service_account = google_service_account.service_account.email

    vpc_access {
        connector = google_vpc_access_connector.my-connector1.id
        egress = "ALL_TRAFFIC"
    }      

  }
}

# AlloyDB Cluster
resource "google_alloydb_cluster" "db" {
  cluster_id   = var.service_name
  location     = var.region
  depends_on = [google_service_networking_connection.default]

  network_config {
    network = google_compute_network.db_network.id
  }

  initial_user {
    password = var.db_password
  }
}

resource "google_alloydb_instance" "db" {
  cluster       = google_alloydb_cluster.db.name
  instance_id   = var.db_instance_name
  instance_type = "PRIMARY"

  machine_config {
    cpu_count = 2
  }

}

# Network for AlloyDB
resource "google_vpc_access_connector" "my-connector1" {
  name         = "${var.service_name}-connector"
  region       = var.region
  network      = google_compute_network.db_network.name
  ip_cidr_range = "10.8.0.0/28"
}

resource "google_compute_network" "db_network" {
  name                    = "${var.service_name}-network"
  auto_create_subnetworks = false
}

resource "google_compute_global_address" "private_ip_address" {
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.db_network.id
}

resource "google_service_networking_connection" "default" {
  network                 = google_compute_network.db_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

resource "google_compute_network_peering_routes_config" "peering_routes" {
  peering = google_service_networking_connection.default.peering
  network = google_compute_network.db_network.name

  import_custom_routes = true
  export_custom_routes = true
}

# Service Account for Cloud Run
resource "google_service_account" "service_account" {
  account_id   = "${var.service_name}-sa"
}

# Permissions
resource "google_project_iam_member" "alloydb_user" {
  project = var.project_id
  role    = "roles/alloydb.client"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}


resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_cloud_run_service_iam_policy" "noauth" {
   location    = google_cloud_run_v2_service.demo_service.location
   project     = google_cloud_run_v2_service.demo_service.project
   service     = google_cloud_run_v2_service.demo_service.name

   policy_data = data.google_iam_policy.noauth.policy_data
}