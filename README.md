# README - MVP Système de Contrôle d'Accès par Badge

## 1. Objectif du MVP
Ce projet propose un système de contrôle d'accès basé sur l'utilisation de badges RFID/NFC. L'objectif est d'assurer une gestion sécurisée des accès à un bâtiment ou une zone réservée en vérifiant les autorisations des utilisateurs et en enregistrant leurs entrées et sorties.

## 2. Fonctionnalités Essentielles

### 🔹 Lecture et validation du badge
- L'utilisateur présente son badge devant un lecteur connecté.
- Le système identifie le badge et vérifie son autorisation dans une base de données.

### 🔹 Vérification des droits d'accès
- **Si le badge est valide et autorisé** ✅ :
  - La porte s'ouvre.
  - L'accès est enregistré.
- **Si le badge est invalide ou refusé** ❌ :
  - La porte reste fermée.
  - Une alerte peut être envoyée.

### 🔹 Enregistrement des accès
- Chaque tentative d'accès est enregistrée :
  - ID du badge
  - Heure de passage
  - Statut de l'accès (autorisation ou refus)
- Un historique des logs permet de suivre les entrées et sorties.

### 🔹 Gestion des erreurs et incidents
- **Badge inconnu ou non autorisé** → Accès refusé.
- **Tentatives échouées consécutives** → Blocage temporaire du badge.
- **Badge désactivé** (perte, vol, fin de contrat) → Accès immédiatement refusé.

## 3. Flux Utilisateur Minimal
1. L'utilisateur badge sur un lecteur 📍
2. Le système vérifie les autorisations 🔍
3. **Si OK** ✅ : La porte s’ouvre et l'accès est enregistré.
4. **Si NON** ❌ : L'accès est refusé et peut générer une alerte.
5. Toutes les tentatives sont enregistrées dans un journal d’accès.

## 4. Cas d'Usage Minimum (6 Use Cases)
- ✅ **Accès autorisé** : Un employé avec un badge valide peut entrer.
- ❌ **Accès refusé** : Un visiteur sans badge ou un employé non autorisé ne peut pas entrer.
- ❌ **Badge désactivé** : Un badge perdu ou volé ne fonctionne plus.
- 🚨 **Tentatives échouées** : Après plusieurs échecs, une alerte est générée.
- 📋 **Enregistrement des passages** : Toutes les entrées et sorties sont tracées.
- 🔒 **Blocage temporaire après plusieurs échecs** : Un badge est suspendu après 3 tentatives infructueuses.

