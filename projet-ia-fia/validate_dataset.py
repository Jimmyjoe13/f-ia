import json
import sys

def validate_jsonl_file(file_path):
    """Valide le format JSONL selon les standards OpenAI"""
    
    print(f"🔍 Validation du fichier: {file_path}")
    
    errors = []
    warnings = []
    line_count = 0
    total_tokens = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line_count += 1
                line = line.strip()
                
                if not line:
                    continue
                
                try:
                    # Parse JSON
                    data = json.loads(line)
                    
                    # Vérifications obligatoires
                    if 'messages' not in data:
                        errors.append(f"Ligne {line_num}: Champ 'messages' manquant")
                        continue
                    
                    messages = data['messages']
                    if not isinstance(messages, list):
                        errors.append(f"Ligne {line_num}: 'messages' doit être une liste")
                        continue
                    
                    # Vérifier structure des messages
                    has_system = False
                    has_user = False
                    has_assistant = False
                    
                    for msg in messages:
                        if not isinstance(msg, dict):
                            errors.append(f"Ligne {line_num}: Message invalide")
                            continue
                        
                        if 'role' not in msg or 'content' not in msg:
                            errors.append(f"Ligne {line_num}: Message sans 'role' ou 'content'")
                            continue
                        
                        role = msg['role']
                        content = msg['content']
                        
                        if role == 'system':
                            has_system = True
                        elif role == 'user':
                            has_user = True
                        elif role == 'assistant':
                            has_assistant = True
                        
                        # Estimation des tokens (approximation)
                        total_tokens += len(content.split()) * 1.3
                    
                    # Vérifications de structure
                    if not has_user:
                        warnings.append(f"Ligne {line_num}: Pas de message 'user'")
                    
                    if not has_assistant:
                        errors.append(f"Ligne {line_num}: Pas de message 'assistant'")
                
                except json.JSONDecodeError as e:
                    errors.append(f"Ligne {line_num}: JSON invalide - {e}")
    
    except FileNotFoundError:
        errors.append(f"Fichier non trouvé: {file_path}")
        return False
    
    # Résultats
    print(f"\n📊 RÉSULTATS DE VALIDATION:")
    print(f"   Lignes traitées: {line_count}")
    print(f"   Tokens estimés: {int(total_tokens):,}")
    print(f"   Erreurs: {len(errors)}")
    print(f"   Avertissements: {len(warnings)}")
    
    if errors:
        print(f"\n❌ ERREURS TROUVÉES:")
        for error in errors[:10]:  # Limiter à 10 erreurs
            print(f"   • {error}")
        if len(errors) > 10:
            print(f"   ... et {len(errors) - 10} autres erreurs")
        return False
    
    if warnings:
        print(f"\n⚠️ AVERTISSEMENTS:")
        for warning in warnings[:5]:
            print(f"   • {warning}")
    
    print(f"\n✅ VALIDATION RÉUSSIE!")
    print(f"   Le fichier est prêt pour OpenAI Fine-tuning")
    print(f"   Coût estimé: ~${(total_tokens / 1000) * 0.008:.2f}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_dataset.py <chemin_fichier.jsonl>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    is_valid = validate_jsonl_file(file_path)  # CORRECTION ICI: validate_jsonl_file au lieu de validate_dataset
    
    if not is_valid:
        print("\n🚫 Corrigez les erreurs avant de continuer!")
        sys.exit(1)
    else:
        print("\n🚀 Prêt pour l'upload sur OpenAI!")
