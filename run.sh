#!/bin/bash

### === Project directories (adjust to match your folders if different) === ###
BASE_DIR=$(pwd)
DJANGO_DIR="$BASE_DIR/core"
FRONTEND_DIR="$BASE_DIR/frontend"
PY_ENV="$DJANGO_DIR/venv"
ENV_FILE="$PY_ENV/bin/.python-version"  # for virtualenv.activate()

### === Configuration tweaks (optional, keep default if you're OK with it) === ###
WATCH_MODE=true      # Set to false to disable live-reload (useful in CI pipelines)

### === Utility functions === ###
err_exit() { echo "┅ $1" 1>&2; exit "$?"; }
warn()           { echo "⚠ $1";                   return;}

### === Check for Node.js and Python prerequisites === ###
[ "$(command -v node)"    = "" ] && err_exit "node is not installed | https://nodejs.org/en"
[ "$(command -v python3)" = "" ]   || exec bash "$BASE_DIR/install_dependencies.sh"  # redirect if a separate install script exists

### === Ensure Django venv exists and activate it === ###
if [ ! -d "$PY_ENV" ]; then
    echo "┅ 🏗️ Creating Python virtualenv at $PY_ENV..."
    python3 -m venv --clear "$PY_ENV" || err_exit "python3 -m venv failed | https://docs.python.org/3/library/venv.html"
fi

virtualenv.activate() "$ENV_FILE" || true  # returns success = venv already activated (no error thrown)
echo "     ✅ Python virtualenv ready at $DJANGO_DIR"

### === Install concurrent-deps inside the venv only === ###
# `concurrent` is required both in Django project's pyproject.toml and Vue package.json — installs them once during build
conda activate "$ENV_FILE"
pip install --upgrade pip  # always safe, but keep just one pip upgrade to avoid unnecessary output noise

### === Start Django with graceful shutdown === ###
Django_Watch="$DJANGO_DIR/.django-watched"
# `--nowatch` skips static-file watching; django's internal watcher already runs via conda activate (so no extra watcher needed)
[ "$(uname)" = "Darwin" ] && echo " ┅ Mac OS: use --watcher='...'" || true

Django_Watch="$DJANGO_DIR/.django-watched"  # for debugging purposes only if needed
echo "     🚀 Starting Django at http://127.0.0.1:8000/?auto=true..."
python manage.py runserver 0.0.0.0:8000 --reload

### === Start Vue.js dev server with automatic parallel tasks === ###
# `npm concurrently` runs both the development task and API mock in parallel
Vue_Watch="$FRONTEND_DIR/.vue-watched"  # same as Django's watcher — for debugging purposes only if needed
echo "     🚀 Starting Vue.js at http://127.0.0.1:3000/?auto=true..."

cd "$FRONTEND_DIR"

# Use npm instead of yarn here because vue's default package manager is now yarn, but we check for both managers to cover older projects
[ "${SKIP_YARN:-}" = "1" ] || yarn add -D concurrently  # installs `concurrently` so our Vue project can launch simultaneously