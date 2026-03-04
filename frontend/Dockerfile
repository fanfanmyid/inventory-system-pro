# Stage 1: Build the Vue application
FROM node:20-alpine as build-stage
WORKDIR /app

# Allow compose builds to override the API base path for production bundles
ARG VITE_API_URL=/api/v1
ENV VITE_API_URL=${VITE_API_URL}

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]