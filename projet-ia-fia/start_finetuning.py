import openai
import os
import time
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def upload_and_finetune(jsonl_file_path):
    """Upload le dataset et lance le fine-tuning"""
    
    # Configuration OpenAI
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai.api_key:
        print("❌ ERREUR: Clé API OpenAI non trouvée!")
        print("   Ajoutez OPENAI_API_KEY à votre fichier .env")
        return
    
    print("🚀 === FINE-TUNING F-IA SUR OPENAI ===\n")
    
    try:
        # 1. Upload du fichier de training
        print("📤 Upload du dataset...")
        with open(jsonl_file_path, 'rb') as f:
            upload_response = openai.File.create(
                file=f,
                purpose='fine-tune'
            )
        
        file_id = upload_response.id
        print(f"✅ Dataset uploadé avec succès!")
        print(f"   File ID: {file_id}")
        print(f"   Taille: {upload_response.bytes} bytes")
        
        # 2. Attendre que le fichier soit traité
        print("\n⏳ Attente du traitement du fichier...")
        while True:
            file_status = openai.File.retrieve(file_id)
            if file_status.status == 'processed':
                print("✅ Fichier traité et prêt!")
                break
            elif file_status.status == 'error':
                print(f"❌ Erreur lors du traitement: {file_status}")
                return
            else:
                print(f"   Status: {file_status.status}...")
                time.sleep(5)
        
        # 3. Créer le job de fine-tuning
        print("\n🤖 Création du job de fine-tuning...")
        finetune_response = openai.FineTuningJob.create(
            training_file=file_id,
            model="gpt-3.5-turbo-1106",  # Modèle recommandé pour le fine-tuning
            hyperparameters={
                "n_epochs": 3,  # Nombre d'époques d'entraînement
                "batch_size": "auto",
                "learning_rate_multiplier": "auto"
            },
            suffix="f-ia-v1"  # Suffixe pour identifier votre modèle
        )
        
        job_id = finetune_response.id
        print(f"✅ Job de fine-tuning créé!")
        print(f"   Job ID: {job_id}")
        print(f"   Modèle base: {finetune_response.model}")
        print(f"   Status: {finetune_response.status}")
        
        # 4. Monitoring du fine-tuning
        print(f"\n📊 Monitoring du fine-tuning...")
        print(f"   Cela peut prendre 10-30 minutes selon la charge OpenAI")
        print(f"   Job ID: {job_id}")
        print(f"\n🔗 Vous pouvez aussi suivre le progrès sur:")
        print(f"   https://platform.openai.com/finetune/{job_id}")
        
        # Monitoring automatique (optionnel)
        monitor_job = input("\n❓ Voulez-vous monitorer automatiquement? (y/n): ")
        
        if monitor_job.lower() == 'y':
            print("\n⏳ Monitoring en cours...")
            start_time = time.time()
            
            while True:
                job_status = openai.FineTuningJob.retrieve(job_id)
                elapsed = int(time.time() - start_time)
                
                print(f"   [{elapsed//60:02d}:{elapsed%60:02d}] Status: {job_status.status}")
                
                if job_status.status == 'succeeded':
                    print(f"\n🎉 FINE-TUNING RÉUSSI!")
                    print(f"   Modèle fine-tuné: {job_status.fine_tuned_model}")
                    print(f"   Durée totale: {elapsed//60}m {elapsed%60}s")
                    
                    # Sauvegarder les infos du modèle
                    with open('model_info.txt', 'w') as f:
                        f.write(f"Modèle F-IA Fine-tuné\n")
                        f.write(f"===================\n")
                        f.write(f"Job ID: {job_id}\n")
                        f.write(f"Modèle: {job_status.fine_tuned_model}\n")
                        f.write(f"Créé le: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Dataset: {jsonl_file_path}\n")
                        f.write(f"Exemples: 79\n")
                        f.write(f"Tokens: ~10,058\n")
                    
                    print(f"   ℹ️ Infos sauvées dans model_info.txt")
                    break
                    
                elif job_status.status == 'failed':
                    print(f"\n❌ ÉCHEC DU FINE-TUNING")
                    print(f"   Erreur: {job_status.error}")
                    break
                    
                elif job_status.status == 'cancelled':
                    print(f"\n⚠️ Fine-tuning annulé")
                    break
                
                time.sleep(30)  # Vérifier toutes les 30 secondes
        else:
            print(f"\n📝 Job lancé! Récupérez le modèle plus tard avec:")
            print(f"   Job ID: {job_id}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print(f"   Vérifiez votre clé API et votre connexion internet")

if __name__ == "__main__":
    upload_and_finetune("f-ia-training-v1.jsonl")
