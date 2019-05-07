#!/usr/bin/env python3
"""
Main module of the server file
"""

# Local modules
import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yaml")

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port="15111", debug=True)
