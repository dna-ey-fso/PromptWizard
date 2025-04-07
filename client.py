import requests

SERVER_URL = "http://127.0.0.1:7000"  # Remplacez par l'URL de votre serveur si nécessaire

def update_task_description(task_description):
    """
    Envoie une requête POST pour mettre à jour uniquement la task_description.
    """
    url = f"{SERVER_URL}/update-config"
    payload = {"config_dict": {"task_description": task_description}}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Task description updated:", response.json())
    except requests.exceptions.RequestException as e:
        print("Failed to update task description:", e)

def get_best_prompt():
    """
    Envoie une requête GET pour récupérer le prompt optimisé.
    """
    url = f"{SERVER_URL}/get-best-prompt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Raw Response:", data)  # Log de la réponse brute
        best_prompt = data.get("best_prompt", "No best prompt available")
        expert_profile = data.get("expert_profile", "No expert profile available")
        print("Best Prompt:", best_prompt)
        print("Expert Profile:", expert_profile)
    except requests.exceptions.RequestException as e:
        print("Failed to get best prompt:", e)

if __name__ == "__main__":
    # Exemple d'utilisation
    task_description = "Optimize the prompt for summarization tasks."  # Remplacez par votre propre description
    print("Sending task description...")
    update_task_description(task_description)

    print("Requesting best prompt...")
    get_best_prompt()
