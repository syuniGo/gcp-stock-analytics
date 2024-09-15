terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

# 创建 VM 实例
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "n2-standard-4"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 30
    }
  }

  network_interface {
    network = "default"
    access_config {
      // 这将给VM一个外部IP
    }
  }

  metadata_startup_script = "sudo apt-get update && sudo apt-get install -y docker.io"

  tags = ["http-server", "https-server"]
}

# 输出 VM 的 IP 地址
output "vm_internal_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].network_ip
}

output "vm_external_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}



resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}