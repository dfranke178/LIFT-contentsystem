#!/bin/bash
# Script to safely start the LIFT webhook server

# Kill any existing server processes
echo "Stopping any existing servers..."
pkill -f "python.*simple_server.py" || true

# Start the simple server
echo "Starting secure webhook server on port 8001..."
python simple_server.py 