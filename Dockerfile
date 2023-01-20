FROM node:17.0.1

#Create folder in container to put our backend in
WORKDIR /usr/src/app/backend

#Copy package json and install dependencies
COPY package.json ./
RUN npm install

#Copy app into container
COPY . .


EXPOSE 8080

CMD ["npm","start"]

