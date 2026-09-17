# 1. DevSecOps : Génération d'un mot de passe fort sans le coder en dur
resource "random_password" "db_password" {
  length  = 16
  special = false # Désactivé pour éviter les bugs d'URL avec SQLAlchemy
}

# 2. Security Group pour protéger PostgreSQL
resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow PostgreSQL traffic ONLY from our VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

# 3. Groupe de sous-réseaux pour la BDD
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [aws_subnet.public_1.id, aws_subnet.public_2.id]
}

# 4. Instance RDS PostgreSQL (Configuration Free Tier)
resource "aws_db_instance" "postgres" {
  identifier             = "${var.project_name}-db"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro" # Éligible niveau gratuit
  allocated_storage      = 20            # 20 Go max pour le niveau gratuit
  
  db_name                = "atlasflow_db"
  username               = "atlasflow_user"
  password               = random_password.db_password.result
  
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  
  publicly_accessible    = false # DevSecOps : Isolée d'Internet
  skip_final_snapshot    = true  # Indispensable pour détruire la DB facilement plus tard sans frais
  
  tags = {
    Name = "${var.project_name}-rds"
  }
}