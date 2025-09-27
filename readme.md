# 📚 Comic Book Project

> **An end-to-end pipeline for creating, generating, and publishing comic books** — from story scripts to final exports.  
> Supports AI-assisted art generation, dynamic panel layouts, dialogue lettering, and an advertisement page template.

---

![Cover placeholder](docs/images/cover.png)

---

## 🚀 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Workflow](#workflow)
5. [Tech Stack](#tech-stack)
6. [Getting Started](#getting-started)
7. [Configuration](#configuration)
8. [Docker & Deployment](#docker--deployment)
9. [API Examples](#api-examples)
10. [Roadmap](#roadmap)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

This project provides a **full-stack comic creation workflow**:

- ✏️ **Script → Storyboard → Panel Layout**
- 🎨 **AI-assisted image generation / custom artwork import**
- 💬 **Dynamic text & speech balloons with auto-wrap**
- 📄 **Page composition with bleed & margins**
- 📢 **Advertisement page template (last page)**
- 📦 **Export to PDF or CBZ**

**Image placeholders for docs:**

- `docs/images/cover.png` — Cover/hero screenshot
- `docs/images/page-layout.png` — Storyboard or panel layout
- `docs/images/generator-ui.png` — Image generation UI
- `docs/images/export-preview.png` — Export preview
- `docs/images/ad-page.png` — Advertisement page template

---

## Features

- Flexible **panel templates** (1–6 per page, splash support)
- Configurable **text wrapping** with gap spacing
- Support for **custom fonts** (stored in `assets/fonts/`)
- Export formats: `PDF (print/web)` and `CBZ`
- Built-in **ad page template** with reserved slot
- **Cloud storage integration** (Google Cloud / AWS S3)
- Ready for **Dockerized deployment**

---

## Architecture

![Architecture placeholder](docs/images/architecture.png)

**Main components**

- **Frontend (React/Next.js)** — UI for writing, storyboarding, editing
- **Backend (FastAPI/Express)** — Handles panel generation, exports, storage
- **Workers (Redis queue)** — For heavy image generation & exports
- **Storage** — Local (`./storage/`) or cloud (GCS / S3)
- **Database (Postgres)** — Metadata (books, pages, panels)

---

## Workflow

1. **Write a Script**
   ```text
   PAGE 1
   Panel 1: A rainy alley, neon signs.
   Dialogue: HERO: "It's too quiet tonight."
   ```
