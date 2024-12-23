@echo off
REM Activer l'environnement virtuel
CALL C:\Users\rodgo\Desktop\TheDerivativeDesk\venv\Scripts\activate

REM Naviguer à la racine du projet
cd /d C:\Users\rodgo\Desktop\TheDerivativeDesk

REM Lancer app.py avec Python
python app.py

REM Garder la fenêtre ouverte pour afficher les erreurs (si nécessaire)
pause
