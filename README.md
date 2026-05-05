# 🎨 generative-studio

A web-based **Generative Studio** that creates **2D images/sketches** and **3D assets** using cloud-based AI APIs — designed to run efficiently on local machines without heavy GPU usage.

---

## 🚀 Project Overview

This project is a **hybrid generative system** where:

* 🧠 **AI Processing (Inference):** Handled via cloud APIs (Fal.ai, Stability AI, Replicate)
* 💻 **Local System (Interface):** Handles UI, API orchestration, and rendering

> ⚡ Built specifically to **preserve local resources (MacBook Air M1)** by avoiding local model loading.

---

## 🧱 Tech Stack

### Backend

* **Python**
* **FastAPI**
* **httpx** (API requests)

### Frontend

* **React (Vite)**
* **Three.js**
* **@react-three/fiber**

### APIs

* **Fal.ai** → 3D generation
* **Stability AI / Fal.ai** → 2D generation

---

## 🧩 Core Features

### 🎨 2D Generation

* Text-to-image generation
* Sketch-to-image (ControlNet-based)
* Background removal (segmentation APIs)
* Returns base64 images for rendering

### 🧊 3D Generation

* Text-to-3D / Image-to-3D
* Fetch and render `.GLB` / `.OBJ` models
* Real-time preview using Three.js
* Download generated assets

### 🖥️ Studio Interface

* Minimalist editor layout:

  * Sidebar → Controls
  * Canvas → Image / 3D Viewer
* Live rendering of generated content
---
✅ Benefits:

* Runs smoothly on low-resource machines
* Faster setup
* Scalable architecture
