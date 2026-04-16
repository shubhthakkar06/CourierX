"""
main.py — CourierX Application Entry Point

Starts the Flask web server which serves both:
  - The REST API  at http://localhost:5000/api/...
  - The frontend  at http://localhost:5000/

Usage:
    source venv/bin/activate
    python main.py
"""

from backend.app import app

if __name__ == '__main__':
    print('\n┌─────────────────────────────────────────────┐')
    print('│  📦  CourierX  ·  Full-Stack Web App       │')
    print('│  🌐  http://localhost:5000                  │')
    print('└─────────────────────────────────────────────┘\n')
    app.run(debug=True, port=5000)
