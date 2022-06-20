#!flask/bin/python
import os

from app import app

app.run(debug=True, host="0.0.0.0", port=os.getenv("FLASK_PORT", 5000))
