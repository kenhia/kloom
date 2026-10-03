#!/usr/bin/env bash
# flyctl for the public site's recipes (docs/deploying.md §Public reader
# site): the app's deploy token, not Ken's login. The token is
# FLY_API_TOKEN in kai's /etc/khomelab/secrets.env (k-homelab store entry
# fly-deploy-token-kloom-reader, krot registry/fly.toml); flyctl reads it
# from the environment, so it is never on a command line. flyctl by full
# path: a non-interactive ssh has no PATH line for it.
set -euo pipefail
secrets=/etc/khomelab/secrets.env
token="$(. "$secrets" 2>/dev/null && printf '%s' "${FLY_API_TOKEN:-}")" || true
if [ -z "$token" ]; then
	echo "no FLY_API_TOKEN in $secrets (k-homelab: bin/apply $(hostname -s) khomelab-secrets)" >&2
	exit 1
fi
export FLY_API_TOKEN="$token"
exec "${FLYCTL:-$HOME/.fly/bin/flyctl}" "$@"
