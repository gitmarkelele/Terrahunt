import openai
from decouple import config

openai.api_key = config("AZURE_API_KEY")
openai.api_base = config("AZURE_API_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2024-05-01-preview"

def evaluer_compatibilite(profil, demande):
    prompt = (
        f"Évalue la compatibilité entre ce profil et cette demande.\n"
        f"Profil: {profil}\n"
        f"Demande: {demande}\n"
        f"Réponds par un score sur 10 et une justification concise."
    )
    response = openai.ChatCompletion.create(
        deployment_id="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=200
    )
    return response['choices'][0]['message']['content']
