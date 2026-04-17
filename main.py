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
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print('\n┌─────────────────────────────────────────────┐')
    print('│  📦  CourierX  ·  Full-Stack Web App       │')
    print(f'│  🌐  http://localhost:{port}                 │')
    print('└─────────────────────────────────────────────┘\n')
    
    # Start order-notification scheduler
    # In debug mode, Flask runs two processes; we only want to start the scheduler in the worker.
    # In production (non-debug), we start it immediately.
    is_reloader = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    if not debug or is_reloader:
        from backend.scheduler import start_scheduler
        start_scheduler()

    app.run(debug=debug, port=port, host='0.0.0.0')
