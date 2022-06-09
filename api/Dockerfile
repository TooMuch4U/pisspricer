FROM node:15.4

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY ./src/package*.json ./

RUN npm ci
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY src .

EXPOSE 8080
CMD [ "node", "server.js" ]
