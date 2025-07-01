FROM node:18-alpine AS react-build

WORKDIR /app/frontend

# Copy React app package files
COPY frontend/my-course-registration-app/package*.json ./
RUN npm install

# Copy React app source and build
COPY frontend/my-course-registration-app/ ./
RUN npm run build

FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ .

# Copy React build files to Flask static folder
COPY --from=react-build /app/frontend/build ./static

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
