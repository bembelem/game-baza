FROM node:20

WORKDIR /app
COPY . /app
COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host"]