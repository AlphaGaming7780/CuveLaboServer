# 📘 Documentation du Projet CuveLabo Server

## 🧾 Présentation

Ce projet est une solution logicielle permettant de contrôler deux laboratoires didactiques de régulation de niveau à distance, via un serveur web (page web) et une API :

- **Tortank** : laboratoire à trois cuves.
- **Carapuce** : laboratoire à une cuve.

Le projet a été réalisé entre **février et mai 2025** par **Trioen Loïc stagiaire de la Haute École en Hainaut (HEH)**, département technique, option **bachelier en électronique**.

> ⚠️ **Consigne de sécurité importante**  
> Il est **strictement interdit d'ouvrir la boîte** du laboratoire **Tortank** ou **Carapuce** lorsqu’ils sont **branchés au secteur**.

Pour toute question, vous pouvez me contacter :  
📧 [trioen.loic@gmail.com](mailto:trioen.loic@gmail.com)

---

## ⚙️ Installation & Utilisation

### 🔧 Prérequis à l'utilisation

- **Python 3.11 ou supérieur** (idéalement 3.13)

> Ce code est conçu pour être exécuté sur un **Raspberry Pi**, avec les capteurs (ADS1115) correctement câblés et fonctionnels.  
> Si les capteurs ne sont pas présents ou mal connectés, une **erreur apparaîtra au lancement** du code.

### 📥 Installation

1. Ouvrir le dossier du projet dans un terminal.
2. Exécuter :
   ```bash
   pip install .
   ```
   > Si vous êtes sur un Raspberry Pi, il peut être nécessaire d’ajouter :
   ```bash
   pip install . --break-system-packages
   ```

3. Lancer l’un des serveurs web :
   ```bash
   TortankWebServer
   # ou
   CarapuceWebServer
   ```

4. Une fois lancé, l’adresse IP du serveur s’affichera dans le terminal (ex. `10.20.30.141:5000` ou `10.20.30.142:5000`).  
   Tapez cette adresse dans un navigateur connecté au **même réseau** que le Raspberry Pi pour accéder à l’interface web.

---

### 🛠️ Prérequis pour la modification du code

- **Python 3.11 ou supérieur**
- **Visual Studio Code** avec l'extension Python
- **Node.js** et **npm**
- **React** (via `npm`)
- Exécuter `npm install` dans le dossier de la page web :
  ```
  src/WebPage/
  ```

### 🧑‍💻 Instructions pour la modification

- Après chaque modification de la page web, exécutez :
  ```bash
  npm run build
  ```
  dans le dossier :
  ```
  src/WebPage/
  ```

- En cas de problème lors de la réinstallation du projet sur le Raspberry Pi, vous pouvez :
  - Supprimer manuellement le dossier installé dans :
    ```
    /home/pi/.local/lib/python3.x/site-packages/
    ```
  - Puis relancer l’installation avec :
    ```bash
    pip install . --break-system-packages
    ```

---

## 📁 Arborescence du projet

Voici les fichiers principaux :

- `src/CarapuceWebServer/__main__.py`  
  Point d’entrée du serveur web pour le laboratoire Carapuce.

- `src/CarapuceWebServer/Carapuce.py`  
  Déclaration de la classe Carapuce.

- `src/TortankWebServer/__main__.py`  
  Point d’entrée du serveur web pour le laboratoire Tortank.

- `src/TortankWebServer/Tortank.py`  
  Déclaration de la classe Tortank.

- `src/Common/LaboBase.py`  
  Classe de base commune aux laboratoires de régulation.

- `src/Common/WebServerBase.py`  
  Implémentation du serveur web Flask.

- `src/WebPage/`  
  Contient les fichiers React de la page web.

- `pyproject.toml`  
  Fichier de configuration du projet Python (build avec Hatch).

---

## ✅ Bonnes pratiques

- Ne jamais exécuter les scripts si le matériel n’est pas correctement branché ou alimenté.
- Toujours vérifier la connexion aux capteurs avant d’exécuter un test.
- Ne pas modifier le serveur sans comprendre son fonctionnement, en particulier la gestion des accès concurrents via file d’attente.

---

## 🗒️ Notes supplémentaires

- L'architecture est **modulaire** : chaque labo a son propre serveur, mais partage des composants communs.
- Le système est extensible et peut facilement être adapté à d'autres configurations matérielles.
