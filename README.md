# Chronograph: Full Stack Temporal Development

### Interactive World History Atlas

![Node.js](https://img.shields.io/badge/Node.js-v18-339933?style=for-the-badge&logo=node.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 📖 Project Overview

**Chronograph** is a full-stack interactive world history atlas designed to transform historical exploration into an immersive, spatial experience.

The application combines a **3D interactive globe**, historical era navigation, narrative-driven exploration, and social discovery features to allow users to explore how the world has changed across time.

This repository contains the development of the **Chronograph web application**. The project evolves through multiple versions, with each stage representing a milestone in bringing the 3D temporal atlas to life.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Node.js v18** | Development environment, package management, and frontend build pipeline |
| **React** | Interactive frontend and application state management |
| **FastAPI** | High-performance Python backend and asynchronous API services |
| **MongoDB** | Document-based storage for historical data and metadata |
| **Python** | Backend development and data processing |

---

# 🌎 Chronograph v. 1.0 - Foundation and 3D Visualization

Version **1.0** focused on establishing the core 3D globe infrastructure and the primary user interface for historical era navigation.

## Work Completed

- Installed and configured **Node.js v18** and npm for frontend dependency management.
- Integrated **FastAPI** to handle high-performance asynchronous land transformation data.
- Configured **MongoDB** for flexible, document-based storage of era milestones and era metadata.
- Established **React components** for the 3D globe rendering engine.
- Implemented **Era Jump** logic to handle state changes between Prehistoric and Modern periods.
- Verified local environment connectivity between the Python backend and React frontend.
- Confirmed **41/41 backend pytest checks passing** to ensure data integrity.

## Result

The application successfully serves the **Chronograph 3D environment**, allowing for smooth historical era jumps and establishing the base infrastructure for advanced discovery features.

---

# 📚 Chronograph v. 1.1 - Story Mode and Social Discovery

Version **1.1** introduced narrative-driven exploration and tools for sharing historical snapshots with a general audience.

## Work Completed

- Developed **Story Mode** to provide curated lessons across key historical eras.
- Engineered the **Dice mechanic** for randomized temporal discovery.
- Implemented **Snapshot Sharing**, allowing users to generate direct links to specific coordinates and time periods.
- Refined UI/UX to move beyond a classroom-focused experience and appeal to a global audience.
- Optimized MongoDB queries to support fast retrieval of bookmark stars and shared playlists.

## Result

Chronograph evolved from a static atlas into a **social discovery platform**, enabling users to not only view history but also curate, bookmark, and share their own temporal findings.

---

# 🏗️ Architectural Components

## NODE.JS

**Node.js** serves as the backbone of the development environment, managing the build pipeline and frontend dependencies to ensure a responsive, modern user experience.

### Responsibilities

- Frontend dependency management
- npm package management
- Development tooling
- Build pipeline
- Local development environment

---

## FASTAPI

**FastAPI** is used for its speed and native support for asynchronous tasks, ensuring the globe transitions stay cinematic even when loading complex historical land data.

### Responsibilities

- REST API services
- Historical data retrieval
- Asynchronous backend operations
- Land transformation data
- Backend validation
- Automated testing

---

## MONGODB

**MongoDB** was selected for its horizontal scalability and flexible schema, which allows the temporal data to grow in density without requiring rigid database migrations.

### Responsibilities

- Era metadata
- Historical milestones
- Bookmark stars
- Shared playlists
- Temporal discovery data
- Document-based storage

---

## REACT

**React** powers the interactive UI, managing the complex state of the 3D globe and era-specific overlays.

### Responsibilities

- Interactive user interface
- 3D globe rendering
- Era navigation
- Application state management
- Historical overlays
- Story Mode
- Snapshot Sharing
- Discovery features

---

# 🔄 Application Architecture

```text
                         CHRONOGRAPH
                    Interactive World History Atlas
                               │
                               ▼
                    ┌────────────────────┐
                    │    React Frontend  │
                    │                    │
                    │  • 3D Globe        │
                    │  • Era Navigation  │
                    │  • Story Mode      │
                    │  • Dice Discovery  │
                    │  • Snapshots       │
                    └─────────┬──────────┘
                              │
                         API Requests
                              │
                              ▼
                    ┌────────────────────┐
                    │   FastAPI Backend  │
                    │                    │
                    │  • Historical Data │
                    │  • Era Logic       │
                    │  • Async Services  │
                    │  • Validation      │
                    └─────────┬──────────┘
                              │
                         Database Queries
                              │
                              ▼
                    ┌────────────────────┐
                    │      MongoDB       │
                    │                    │
                    │  • Era Metadata    │
                    │  • Milestones      │
                    │  • Bookmarks       │
                    │  • Playlists       │
                    └────────────────────┘

                    Development Environment
                              │
                              ▼
                    ┌────────────────────┐
                    │     Node.js v18    │
                    │        + npm       │
                    └────────────────────┘
