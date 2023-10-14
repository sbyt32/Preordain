FROM node:20-alpine3.17

WORKDIR /app

COPY . /app

# Refers to "Clean Install"
RUN npm ci
RUN npm run build
RUN rm -rf src/ static/

# ENTRYPOINT ["npm", "run", "dev"]
CMD [ "node", "build/index.js" ]
