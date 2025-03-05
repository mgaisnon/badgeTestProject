# Use Case : Contrôle d’accès par badge

## Titre  
🔹 Vérification et autorisation d’accès via un badge  

## Acteurs  
- **Utilisateur** (Employé, Visiteur, Prestataire, etc.)  
- **Système de contrôle d’accès**  
- **Porte sécurisée**  

## Préconditions  
- Le système de contrôle d’accès est **opérationnel**.  
- Le **lecteur de badge** est connecté au système.  

## Déroulement du scénario  
1. **ETANT DONNE** un utilisateur avec un **badge valide ou invalide**  
2. **QUAND** il présente son badge devant le lecteur  
3. **ALORS** le système scanne et vérifie les droits d’accès du badge  
   - **Si le badge est valide** ✅  
     - ALORS le système envoie un message à la porte : **"Ouvrir"**  
   - **Si le badge est invalide** ❌  
     - ALORS le système envoie un message à la porte : **"Accès refusé"**  

## Postconditions  
- **Cas OK** ✅ : L’utilisateur accède à la zone et la porte s’ouvre.  
- **Cas NON** ❌ : L’accès est bloqué et la porte reste fermée.  
