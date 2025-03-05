# Use Case : Contrôle d’accès par badge

## Titre  
🔹 Vérification et autorisation d’accès via un badge  

## Acteurs  
- **Utilisateur** (Employé, Visiteur, Prestataire, etc.)  
- **Système de contrôle d’accès**  
- **Porte sécurisée**  

## Préconditions  
- Le système de contrôle d’accès est **opérationnel**.  
- L’utilisateur dispose d’un **badge actif ou inactif**.  
- Le **lecteur de badge** est connecté au système.  

## Déroulement du scénario  
1. **ETANT DONNE** un utilisateur qui présente son badge devant le lecteur  
2. **QUAND** le système scanne et vérifie les droits d’accès du badge  
   - **Si le badge est valide**
     - ALORS la porte s’ouvre  
     - ET l’accès est enregistré dans le journal du système  
   - **Si le badge est invalide**  
     - ALORS l’accès est refusé  
     - ET la porte reste fermée  
     - ET une alerte peut être envoyée si nécessaire (ex. tentative multiple)  

## Postconditions  
- **Cas OK** : L’utilisateur accède à la zone et l’événement est enregistré.  
- **Cas NON** : L’accès est bloqué et un message d’erreur est généré.  
