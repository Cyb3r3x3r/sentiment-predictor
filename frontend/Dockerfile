FROM node:18 as build

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

# Serving with lightweight server
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]