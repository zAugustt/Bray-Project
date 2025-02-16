# frontend/Dockerfile
# Use an official Node.js image
FROM node:18-alpine

WORKDIR /app

# Isolate once in prod
COPY package.json /app
COPY package-lock.json /app

# Isolate once in prod
# COPY public/ /app/public
# COPY src/ /app/src 
COPY . .

RUN npm install
RUN npm run build
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
