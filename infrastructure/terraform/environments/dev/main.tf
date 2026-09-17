resource "local_file" "atlasflow_info" {
  filename = "${path.module}/atlasflow_local_test.txt"
  content  = "Bienvenue dans l'Infrastructure as Code d'AtlasFlow !\nCe fichier a été généré par Terraform le ${timestamp()}."
}

data "aws_caller_identity" "current" {}