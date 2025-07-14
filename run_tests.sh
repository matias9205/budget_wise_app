#!/bin/bash

export PYTHONPATH=$(pwd)

echo "🚀 Ejecutando tests con pytest..."
pytest app/tests -v -s
# pytest app/tests -v