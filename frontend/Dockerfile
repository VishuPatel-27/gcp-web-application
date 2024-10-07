# Use an official Node runtime as the base image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependeclsncies
RUN npm install

# Copy the rest of the application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose the port the app runs on
EXPOSE 3000

# Set default environment variable
ENV FLASK_SERVER_URL=http://flask-server:5000

# Define the command to run the app
CMD ["npm", "start", "server.js"]