from locust import HttpUser, task, between

class FlaskAppUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre 1-3 secondes entre chaque requête
    
    @task(2)  # Poids de 2 pour cette tâche (sera appelée deux fois plus souvent)
    def hello_world(self):
        """Test de l'endpoint principal"""
        with self.client.get("/") as response:
            if response.status_code != 200:
                response.failure(f"Status code incorrect: {response.status_code}")
            else:
                # Vérifie que la réponse contient les champs attendus
                data = response.json()
                if not all(key in data for key in ['message', 'status', 'environment']):
                    response.failure("Réponse JSON manquante ou incomplète")

    @task(1)  # Poids de 1 pour cette tâche
    def health_check(self):
        """Test de l'endpoint health"""
        with self.client.get("/health") as response:
            if response.status_code != 200:
                response.failure(f"Status code incorrect: {response.status_code}")
            else:
                data = response.json()
                if 'status' not in data or data['status'] != 'healthy':
                    response.failure("Health check invalide") 