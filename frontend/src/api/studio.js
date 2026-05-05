import axios from 'axios'

const api = axios.create({ baseURL: '' })

// ── 2D ────────────────────────────────────────────────────────────────────────

export const generateImage = (prompt, width = 1024, height = 1024, model = 'flux') =>
  api.post('/generate-2d', { prompt, width, height, model })

export const sketchToImage = (prompt, image_base64, guidance_scale = 7.5) =>
  api.post('/generate-2d/sketch-to-image', { prompt, image_base64, guidance_scale })

export const removeBackground = (image_base64) =>
  api.post('/generate-2d/remove-background', { image_base64 })

// ── 3D ────────────────────────────────────────────────────────────────────────

export const generate3DFromText = (prompt) =>
  api.post('/generate-3d/from-text', { prompt, width: 1024, height: 1024 })

export const generate3DFromImage = (image_base64) =>
  api.post('/generate-3d/from-image', { image_base64 })

export const getDownloadUrl = (url, filename = 'model.glb') =>
  `/generate-3d/download?url=${encodeURIComponent(url)}&filename=${filename}`