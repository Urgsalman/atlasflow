output "file_created_path" {
  value = local_file.atlasflow_info.filename
}

output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnets" {
  value = [aws_subnet.public_1.id, aws_subnet.public_2.id]
}

output "ecr_repository_urls" {
  description = "URLs des dépôts ECR"
  value = {
    for k, v in aws_ecr_repository.services : k => v.repository_url
  }
}

output "db_endpoint" {
  description = "Adresse de connexion de la base de données RDS"
  value       = aws_db_instance.postgres.endpoint
}

output "db_password" {
  description = "Mot de passe généré pour RDS (MASQUÉ par défaut)"
  value       = random_password.db_password.result
  sensitive   = true # DevSecOps : Cache le mot de passe dans la console !
}

output "sqs_queue_url" {
  description = "URL de la file d'attente SQS principale"
  value       = aws_sqs_queue.order_events.url
}

output "github_actions_role_arn" {
  description = "L'ARN du rôle IAM à configurer dans GitHub Actions"
  value       = aws_iam_role.github_actions.arn
}
