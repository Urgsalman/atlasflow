# Utilisation du module officiel AWS EKS pour simplifier la création
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.project_name}-cluster"
  cluster_version = "1.30"

  # Autorise la connexion au cluster depuis ton PC local
  cluster_endpoint_public_access  = true

  vpc_id                   = aws_vpc.main.id
  subnet_ids               = [aws_subnet.public_1.id, aws_subnet.public_2.id]
  
  # Configuration des Worker Nodes (Les machines qui font tourner tes conteneurs)
  eks_managed_node_groups = {
    main = {
      min_size     = 1
      max_size     = 2
      desired_size = 1
      
      # t3.small est un bon compromis pour une démo
      instance_types = ["t3.small"]
    }
  }

  tags = {
    Environment = var.environment
  }
}