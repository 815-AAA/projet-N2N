import spacy

# Chargement du modèle spaCy pour le français
nlp = spacy.load('fr_core_news_lg')

def extraire_A_et_B(phrase):
    """
    Étape 1 du projet : Parseur des séparateurs prépositionnels.
    Extrait les termes A et B d'une forme "A de B" en ignorant les déterminants.
    """
    doc = nlp(phrase)
    
    split_idx = -1
    # 1. Trouver le séparateur (la préposition "de" sous toutes ses formes)
    for i, token in enumerate(doc):
        # SpaCy lemmatise intelligemment "du" en "de" + "le", et "des" en "de" + "les"
        # Il gère aussi "d'" comme un token distinct ayant pour lemme "de"
        if token.pos_ == "ADP" and token.lemma_ == "de":
            split_idx = i
            break
        # Sécurité supplémentaire au cas où le tagger se trompe
        elif token.text.lower() in ["de", "d'", "d’", "du", "des"]:
            split_idx = i
            break
            
    if split_idx == -1:
        return None, None # Pas de structure "A de B" trouvée

    # 2. Extraire A (tous les mots avant "de" qui ne sont pas des déterminants ou ponctuation)
    mots_A = []
    for token in doc[:split_idx]:
        if token.pos_ not in ["DET", "PUNCT"]:
            mots_A.append(token.text)
            
    # 3. Extraire B (tous les mots après "de" qui ne sont pas des déterminants ou ponctuation)
    mots_B = []
    for token in doc[split_idx+1:]:
        if token.pos_ not in ["DET", "PUNCT"]:
            mots_B.append(token.text)
            
    A = " ".join(mots_A).strip()
    B = " ".join(mots_B).strip()
    
    return A, B

def main():
    # Exemples tirés de votre tableau blanc et du PDF
    phrases_test = [
        "Le psy de la voisine",
        "La présentation de l'étudiant",
        "La malice du chien",
        "La maladie d'Alzheimer",
        "saucisse de toulouse",
        "désert d'Algérie",
        "tabouret de bois"
    ]
    
    print("--- ÉTAPE 1 : PARSEUR DE SÉPARATEURS PRÉPOSITIONNELS ---\n")
    
    for phrase in phrases_test:
        A, B = extraire_A_et_B(phrase)
        if A and B:
            print(f"Phrase originale : '{phrase}'")
            print(f"-> A = '{A}' | B = '{B}'\n")
        else:
            print(f"Phrase originale : '{phrase}' -> ÉCHEC DE L'EXTRACTION\n")

if __name__ == "__main__":
    main()