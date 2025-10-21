#!/usr/bin/env python3
"""
Script per avviare l'applicazione Flask

Usage:
    python run.py                    # Avvia in modalità development
    python run.py --prod             # Avvia in modalità production
"""
import os
from app import create_app

# Determina l'ambiente
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Avvia il server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(env == 'development')
    )
