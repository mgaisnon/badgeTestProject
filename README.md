# README - Système de Contrôle d'Accès par Badge

## Développeurs

Paul CARION - @farkza
Nicolas DAUNAC - @Farfadeli
Yassin FARASSI - @yassin312
Mathieu GAISNON - @mgaisnon
Baptiste MANCEL - @NovemIgnotum
Julie MONTOUX - @JulieMontoux

## Fonctionnalité

Le système de contrôle d'accès par badge permet de gérer les accès à différentes portes en utilisant des badges. Chaque porte a une liste de badges autorisés (whitelist) et une liste de badges interdits (blacklist). Lorsqu'un badge est scanné, le système vérifie si ce badge est valide selon les règles suivantes :

- Si le badge est dans la whitelist, l'accès est accordé.
- Si le badge est dans la blacklist, l'accès est refusé.
- Si le badge n'est ni dans la whitelist ni dans la blacklist, l'accès est refusé.

Le système peut également gérer des **badges temporaires** et un **mode urgence** qui permet d'ouvrir la porte sans badge.

### Fonctionnalités principales

- **Whitelist** : Liste de badges autorisés.
- **Blacklist** : Liste de badges interdits.
- **Badges temporaires** : Permet d'ajouter des badges pour un accès temporaire.
- **Mode urgence** : Permet d'ouvrir la porte sans vérification du badge.
- **Double validation** : En mode sécurisé, un badge doit être scanné deux fois pour permettre l'ouverture de la porte.

## Tests / Cas d'utilisation

### 1. Test du badge valide

**Description** : Vérifie qu’un badge valide dans la whitelist ouvre la porte.

- **Scénario** : Badge `1234` dans la whitelist.

### 2. Test du badge invalide

**Description** : Vérifie qu’un badge qui ne se trouve pas dans la whitelist ne permet pas l’accès.

- **Scénario** : Badge `4321` qui n'est pas dans la whitelist.

### 3. Test d’un badge zéro

**Description** : Vérifie le comportement d’un badge ayant la valeur zéro.

- **Scénario** : Badge `0`.

### 4. Test du badge temporaire

**Description** : Vérifie que l'accès est autorisé avec un badge temporaire et que l’accès est refusé lorsque ce badge expire.

- **Scénario** : Badge temporaire ajouté, puis expiré.

### 5. Test du mode urgence

**Description** : Vérifie que lorsque le mode urgence est activé, la porte s’ouvre sans badge.

- **Scénario** : Mode urgence activé et badge non nécessaire.

### 6. Test de la double validation

**Description** : Vérifie que le badge scanné deux fois dans une porte en mode sécurisé ouvre bien la porte.

- **Scénario** : Badge `1234` scanné deux fois sur une porte en mode sécurisé.

### 7. Test de l’ajout et retrait d’un badge de la whitelist

**Description** : Vérifie l’ajout et le retrait d’un badge dans la whitelist et l’effet sur l’accès.

- **Scénario** : Badge ajouté à la whitelist, puis retiré, puis testé pour l'accès.

### 8. Test du badge en double dans la whitelist

**Description** : Vérifie le comportement si un badge est en double dans la whitelist.

- **Scénario** : Badge `1234` ajouté deux fois dans la whitelist.

### 9. Test de la whitelist vide

**Description** : Vérifie que l’accès est refusé si la whitelist est vide.

- **Scénario** : Whitelist vide et badge `1234`.

### 10. Test du retrait du badge après utilisation

**Description** : Vérifie que l’accès est refusé après le retrait d’un badge de la whitelist.

- **Scénario** : Badge retiré après première utilisation.

### 11. Test d’un badge `None` dans la whitelist

**Description** : Vérifie que l’accès est refusé si un badge `None` est ajouté à la whitelist.

- **Scénario** : Badge `None` ajouté à la whitelist.

### 12. Test d’un type incorrect (chaîne de caractères)

**Description** : Vérifie que l’accès est refusé si un badge est une chaîne de caractères.

- **Scénario** : Badge `"ABC"`.

### 13. Test d’un type incorrect (dictionnaire)

**Description** : Vérifie que l’accès est refusé si un badge est un dictionnaire.

- **Scénario** : Badge `{}`.

### 14. Test de plusieurs badges successifs

**Description** : Vérifie que l’accès est accordé pour chaque badge détecté successivement.

- **Scénario** : Badge `1234` puis `5678` successivement.

### 15. Test des scans rapides de badges

**Description** : Vérifie que plusieurs scans rapides avec un badge valide fonctionnent correctement.

- **Scénario** : Badge `1234` scanné rapidement 10 fois.

### 16. Test de l’ajout d’un badge après initialisation

**Description** : Vérifie que l’ajout d’un badge après l'initialisation fonctionne correctement.

- **Scénario** : Badge `8881` ajouté après initialisation et scanné.

### 17. Test du retrait d’un badge de la whitelist

**Description** : Vérifie que le retrait d’un badge de la whitelist empêche l’accès.

- **Scénario** : Badge `1234` retiré de la whitelist.

### 18. Test du multithreading des scans de badges

**Description** : Vérifie que plusieurs scans de badges en multithreading fonctionnent correctement.

- **Scénario** : Scans de badges simultanés via des threads.

### 19. Test de la surcharge du système avec des badges incorrects

**Description** : Vérifie le comportement du système lorsque de nombreux badges incorrects sont scannés.

- **Scénario** : Badge `9999` scanné 100 fois.

### 20. Test de panne du lecteur

**Description** : Vérifie le comportement du système lorsque le lecteur est en panne.

- **Scénario** : Lecteur est `None`.

### 21. Test de panne de la porte

**Description** : Vérifie le comportement du système lorsque la porte est en panne.

- **Scénario** : Porte est `None`.

### 22. Test du badge détecté après un timeout

**Description** : Vérifie le comportement du système lorsque le badge est détecté après un délai.

- **Scénario** : Badge `5678` détecté après une pause de 2 secondes.

### 23. Test d’un badge dans la blacklist

**Description** : Vérifie que l’accès est refusé si un badge est dans la blacklist.

- **Scénario** : Badge `9999` dans la blacklist.

### 24. Test de la priorité de la blacklist sur la whitelist

**Description** : Vérifie que la blacklist a priorité sur la whitelist.

- **Scénario** : Badge `8888` dans la whitelist et blacklist.

### 25. Test de l’historique des accès

**Description** : Vérifie que l’historique des accès est mis à jour correctement.

- **Scénario** : Badge `1234` scanné et ajouté à l’historique des accès.

### 26. Test de l’historique des refus

**Description** : Vérifie que l’historique des refus est mis à jour correctement.

- **Scénario** : Badge `4321` scanné et ajouté à l’historique des refus.

### 27. Test des trois échecs consécutifs

**Description** : Vérifie que l'alarme est déclenchée après trois échecs consécutifs avec des badges incorrects.

- **Scénario** : Badge `4321` scanné trois fois.

### 28. Test du mode sécurisé avec double validation

**Description** : Vérifie le comportement d’une porte en mode sécurisé avec double validation.

- **Scénario** : Badge `1234` scanné deux fois.

### 29. Test de l’ajout d’un badge temporaire

**Description** : Vérifie que l’ajout d’un badge temporaire permet l’accès.

- **Scénario** : Badge temporaire `7777` ajouté et scanné.

### 30. Test de l’expiration d’un badge temporaire

**Description** : Vérifie que l’accès est refusé après l’expiration d’un badge temporaire.

- **Scénario** : Badge `7777` expiré et scanné.

### 31. Test de l’ajout et retrait d’un badge temporaire

**Description** : Vérifie le fonctionnement de l’ajout et retrait d’un badge temporaire.

- **Scénario** : Badge `1234` ajouté, retiré, puis scanné.

### 32. Test de la réinitialisation de l’historique

**Description** : Vérifie que l’historique des accès et refus est réinitialisé.

- **Scénario** : Historique réinitialisé après un badge scanné.

### 33. Test du mode urgence avec activation de tous les contrôles

**Description** : Vérifie que tous les contrôles sont désactivés en mode urgence.

- **Scénario** : Mode urgence activé et badge `9999` scanné.

### 34. Test de l’alarme après trois échecs consécutifs

**Description** : Vérifie que l'alarme se déclenche après trois échecs consécutifs.

- **Scénario** : Badge `4321` scanné trois fois.

### 35. Test du réajout d’un badge dans la whitelist

**Description** : Vérifie le réajout d’un badge dans la whitelist après retrait.

- **Scénario** : Badge `1234` retiré puis réajouté.

### 36. Test de l’alarme active et de l’accès refusé

**Description** : Vérifie que l’accès est refusé lorsque l’alarme est active.

- **Scénario** : Alarme activée et badge valide scanné.
