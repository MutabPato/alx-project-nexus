# 🎬 Movie Recommendation Backend – Project Nexus (ProDev BE)

Welcome to the Movie Recommendation App backend, developed as part of the **Project Nexus Capstone** in the ProDev Backend Web Developer Program. This project demonstrates core backend engineering skills including API development, authentication, performance optimization, caching, and documentation.

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Caching with Redis](#caching-with-redis)
- [Documentation](#documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Presentation & Demo](#presentation--demo)
- [License](#license)

---

## 📖 Project Overview

The Movie Recommendation Backend is a Django-based RESTful API that:

- Fetches trending and recommended movies from [TMDb](https://www.themoviedb.org/)
- Allows users to register, log in, and save favorite movies
- Implements JWT authentication and Redis caching for performance
- Follows industry best practices in API design, documentation, and deployment

---

## 🌟 Features

- ✅ User registration and login (JWT)
- 🎞️ Fetch trending and recommended movies from TMDb
- 💾 Save, view, and delete favorite movies
- 🚀 Redis caching for fast movie data retrieval
- 📄 Swagger/OpenAPI documentation
- 🔐 Secure authentication and route protection
- 🧪 Unit & integration testing
- 🐳 Docker-ready setup (optional)

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django** | Web framework for backend API |
| **Django REST Framework** | RESTful API development |
| **PostgreSQL** | Relational database |
| **Redis** | In-memory caching system |
| **JWT** | Secure authentication |
| **TMDb API** | Movie data source |
| **Swagger (drf-yasg)** | API documentation |
| **Docker** | Containerization (optional) |

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/MutabPato/alx-project-nexus.git
cd alx-project-nexus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
