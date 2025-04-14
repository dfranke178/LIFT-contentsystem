#!/bin/bash
# Script to safely start the LIFT secure webhook server

# Kill any existing server processes
echo "Stopping any existing servers..."
pkill -f "python.*secure_server.py" || true

# Start the secure server
echo "Starting secure webhook server on port 8005..."
python secure_server.py 