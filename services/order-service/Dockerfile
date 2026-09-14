# 1. Utiliser une image de base officielle, légère (slim)
FROM python:3.10-slim

# 2. Sécurité : Créer un utilisateur non-root
RUN addgroup --system appgroup && adduser --system --group appuser

# 3. Définir le répertoire de travail
WORKDIR /app

# 4. Copier uniquement les requirements en premier (optimisation du cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier le reste du code
COPY . .

# 6. Sécurité : Donner la propriété des fichiers au nouvel utilisateur
RUN chown -R appuser:appgroup /app

# 7. Basculer sur l'utilisateur non-root
USER appuser

# 8. Exposer le port
EXPOSE 8000

# 9. Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]