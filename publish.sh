#!/bin/bash
source .env
twine upload dist/* --username __token__ --password "$TWINE_TOKEN"
