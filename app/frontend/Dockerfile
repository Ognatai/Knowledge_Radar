# Build the chat UI, then serve it with nginx, which forwards /api to the api container.
FROM node:22-alpine AS build
WORKDIR /frontend
COPY app/frontend/package.json app/frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY app/frontend/ ./
RUN npm run build

FROM nginx:1.27-alpine
COPY app/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /frontend/dist /usr/share/nginx/html
