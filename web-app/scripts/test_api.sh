#!/bin/bash

curl -X POST http://localhost:5000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Olá, como você está?"}'
