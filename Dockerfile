# The public reader site's image (docs/deploying.md §Public reader site,
# korg 3503): the reader edition, its admin CLI, and the library and media
# `just stage-public` put in build-public/. Built and pushed by
# `just publish-public`, on kai, from a clean main.
#
# Layers run from what changes least to what changes most, and the library
# and media come last, so a content-only publish pushes only those.

# The reader edition, built here from the source the image ships.
FROM node:24-slim AS build
WORKDIR /src
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund --loglevel=error
COPY . .
# The commit, for About: the build context has no .git.
ARG KLOOM_BUILD=""
RUN KLOOM_EDITION=reader KLOOM_BUILD="$KLOOM_BUILD" npx svelte-kit sync \
	&& KLOOM_EDITION=reader KLOOM_BUILD="$KLOOM_BUILD" npx vite build

# What the server imports at run time: adapter-node leaves `dependencies` out of its bundle.
FROM node:24-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --ignore-scripts --no-audit --no-fund --loglevel=error

FROM node:24-slim
WORKDIR /app
ENV NODE_ENV=production \
	KLOOM_EDITION=reader \
	HOST=0.0.0.0 \
	PORT=8080 \
	KLOOM_CONTENT_DB=/app/content.db \
	KLOOM_MEDIA_DIR=/app/media \
	KLOOM_DATA_DIR=/data
COPY --from=deps /app/node_modules node_modules
COPY package.json serve.js admin.mjs ./
# admin.mjs opens these with plain Node; they import nothing but node: modules.
COPY src/lib/server/accounts.ts src/lib/server/sqlite-reader-store.ts src/lib/server/
COPY --from=build /src/build-reader build-reader
COPY build-public/media media
COPY build-public/content.db content.db
EXPOSE 8080
# Root inside the machine: Fly mounts the volume at /data owned by root.
CMD ["node", "serve.js"]
