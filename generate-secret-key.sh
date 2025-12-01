#!/bin/sh
if [ -z "$DJANGO_SECRET_KEY" ]; then
    export DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    echo "Generated SECRET_KEY: $DJANGO_SECRET_KEY"
fi

