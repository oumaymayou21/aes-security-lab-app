#  AES Security Toolkit

##  Description
Ce projet est une application Python en ligne de commande permettant d'explorer les différents modes de chiffrement AES et d'analyser leurs vulnérabilités en pratique.

Il met en évidence le fait que la sécurité dépend non seulement de l'algorithme (AES), mais surtout de la manière dont il est utilisé.

---

##  Objectifs
- Comprendre le fonctionnement du chiffrement AES
- Comparer les modes ECB, CBC, CTR et GCM
- Identifier les failles de sécurité associées
- Simuler des attaques réelles
- Implémenter le chiffrement et déchiffrement de fichiers

---

## Fonctionnalités

###  Modes AES
- ECB (non sécurisé)
- CBC
- CTR
- GCM (authentifié et sécurisé)

###  Attaques implémentées
- Bit Flipping Attack
- ECB Pattern Leak Attack
- Nonce Reuse Attack (CTR/GCM)

###  Gestion de fichiers
- Chiffrement de fichiers
- Déchiffrement de fichiers
- Détection de modification (GCM)

---

##  Utilisation

### Installation
```bash
pip install -r requirements.txt