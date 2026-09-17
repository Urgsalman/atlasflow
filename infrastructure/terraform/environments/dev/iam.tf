# 1. Fournisseur d'identité OIDC (AWS fait confiance à GitHub)
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  # Empreintes SSL officielles de GitHub
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1", "1c58a3a8518e8759bf075b76b750d4f2df264fcd"] 
}

# 2. Le Rôle IAM que GitHub pourra assumer temporairement
resource "aws_iam_role" "github_actions" {
  name = "${var.project_name}-github-actions-role"

  # DevSecOps : Seul TON dépôt GitHub précis a le droit d'assumer ce rôle
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity"
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_username}/${var.project_name}:*"
          }
        }
      }
    ]
  })
}

# 3. DevSecOps : Politique de moindre privilège (Accès strict à ECR uniquement)
resource "aws_iam_role_policy" "github_actions_ecr" {
  name = "${var.project_name}-ecr-push-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "ecr:GetAuthorizationToken"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetRepositoryPolicy",
          "ecr:DescribeRepositories",
          "ecr:ListImages",
          "ecr:DescribeImages",
          "ecr:BatchGetImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ]
        # Limite l'accès uniquement aux 3 dépôts ECR que nous avons créés
        Resource = [for repo in aws_ecr_repository.services : repo.arn]
      }
    ]
  })
}