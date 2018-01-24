export PYTHONPATH="$HOME:$PYTHONPATH"
gunicorn \
    -w 10 \
    --timeout 120 \
    -b 0.0.0.0:22399 \
    --limit-request-line 0 \
    --access-logfile $HOME/mihawk/logs/access.log \
    --error-logfile $HOME/mihawk/logs/error.log \
    --log-level info \
    --worker-class=meinheld.gmeinheld.MeinheldWorker \
    -D \
    app:app
