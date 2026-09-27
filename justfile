# Windows: `just` runs recipes through `sh`, which Windows does not ship — put
# Git for Windows' `usr\bin` on PATH (it holds `sh.exe`) or run from Git Bash.
# (Upstream's own requirement: "sh must be available in the PATH".)

# List available recipes
default:
    @just --list

# Run type checks, formatting/lint checks and unit tests (content validation
# included: the western-civ subject is loaded and validated by a test)
check:
    npm run check
    npm run lint
    npm test

# Serve locally on loopback
dev:
    npm run dev

# Build the Node server
build:
    npm run build
