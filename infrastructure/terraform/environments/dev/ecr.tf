# 1. Définition de nos microservices
locals {
  services = ["order-service", "inventory-service", "notification-service"]
}

# 2. Création des dépôts ECR avec boucle for_each
resource "aws_ecr_repository" "services" {
  for_each             = toset(local.services)
  name                 = "${var.project_name}-${each.key}"
  image_tag_mutability = "MUTABLE"
  
  # Très important pour pouvoir tout détruire facilement à la fin du projet
  force_delete = true 

  # DEVSECOPS : Active le scan gratuit des vulnérabilités des images Docker
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-${each.key}"
  }
}

# 3. Règle de cycle de vie pour garantir la gratuité (Garde uniquement les 3 dernières images)
resource "aws_ecr_lifecycle_policy" "cleanup" {
  for_each   = toset(local.services)
  repository = aws_ecr_repository.services[each.key].name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Garder uniquement les 3 images les plus récentes pour éviter les coûts"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 3
      }
      action = {
        type = "expire"
      }
    }]
  })
}