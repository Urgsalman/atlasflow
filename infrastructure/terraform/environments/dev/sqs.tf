# 1. La Dead Letter Queue (DLQ) pour stocker les messages en échec
resource "aws_sqs_queue" "order_events_dlq" {
  name = "${var.project_name}-order-events-dlq"
  
  tags = {
    Name = "${var.project_name}-dlq"
  }
}

# 2. La file d'attente principale (Main Queue)
resource "aws_sqs_queue" "order_events" {
  name = "${var.project_name}-order-events-queue"

  # Le temps alloué à un service pour traiter le message (30 secondes par défaut)
  visibility_timeout_seconds = 30 

  # Redrive Policy : Si un message échoue 3 fois, on l'envoie dans la DLQ
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_events_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Name = "${var.project_name}-queue"
  }
}