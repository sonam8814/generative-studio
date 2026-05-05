import { useState, useCallback } from 'react'
import Sidebar from './components/Sidebar'
import Canvas2D from './components/Canvas2D'
import Viewer3D from './components/Viewer3D'
import StatusBar from './components/StatusBar'
import { generateImage, generate3DFromText, removeBackground, getDownloadUrl } from './api/studio'

export default function App() {
  const [loading, setLoading]         = useState(false)
  const [status, setStatus]           = useState('')
  const [error, setError]             = useState('')
  const [imageBase64, setImageBase64] = useState(null)
  const [modelUrl, setModelUrl]       = useState(null)
  const [activeView, setActiveView]   = useState('2d') // '2d' | '3d'
  const [lastModelUrl, setLastModelUrl] = useState(null)

  const showStatus = (msg) => { setStatus(msg); setError('') }
  const showError  = (msg) => { setError(msg);  setStatus('') }
  const clearMsg   = ()    => { setStatus('');  setError('') }

  // ── Generate 2D ─────────────────────────────────────────────────────────────
  const handleGenerate2D = useCallback(async ({ prompt, model, width, height }) => {
    setLoading(true)
    setActiveView('2d')
    showStatus('Generating image...')
    try {
      const res = await generateImage(prompt, width, height, model)
      setImageBase64(res.data.image_base64)
      showStatus('Image ready!')
      setTimeout(clearMsg, 2500)
    } catch (e) {
      showError(e.response?.data?.detail || 'Generation failed')
    } finally {
      setLoading(false)
    }
  }, [])

  // ── Remove Background ────────────────────────────────────────────────────────
  const handleRemoveBg = useCallback(async () => {
    if (!imageBase64) return showError('Generate an image first')
    setLoading(true)
    showStatus('Removing background...')
    try {
      const res = await removeBackground(imageBase64)
      setImageBase64(res.data.image_base64)
      showStatus('Background removed!')
      setTimeout(clearMsg, 2500)
    } catch (e) {
      showError(e.response?.data?.detail || 'Background removal failed')
    } finally {
      setLoading(false)
    }
  }, [imageBase64])

  // ── Generate 3D ─────────────────────────────────────────────────────────────
  const handleGenerate3D = useCallback(async ({ prompt }) => {
    setLoading(true)
    setActiveView('3d')
    showStatus('Step 1/2 — Generating base image via Pollinations...')
    try {
      showStatus('Step 2/2 — Building 3D model (may take ~60s)...')
      const res = await generate3DFromText(prompt)
      const url = res.data.model_url
      setLastModelUrl(url)
      setModelUrl(url)
      if (res.data.intermediate_image_base64) {
        setImageBase64(res.data.intermediate_image_base64)
      }
      showStatus('3D model ready!')
      setTimeout(clearMsg, 2500)
    } catch (e) {
      showError(e.response?.data?.detail || '3D generation failed')
    } finally {
      setLoading(false)
    }
  }, [])

  // ── Download PNG ─────────────────────────────────────────────────────────────
  const handleDownloadPNG = () => {
    if (!imageBase64) return
    const a = document.createElement('a')
    a.href = `data:image/png;base64,${imageBase64}`
    a.download = 'generated.png'
    a.click()
  }

  // ── Download GLB ─────────────────────────────────────────────────────────────
  const handleDownloadGLB = () => {
    if (!lastModelUrl) return
    const a = document.createElement('a')
    a.href = getDownloadUrl(lastModelUrl, 'model.glb')
    a.download = 'model.glb'
    a.click()
  }

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>

      {/* Sidebar */}
      <Sidebar
        onGenerate2D={handleGenerate2D}
        onGenerate3D={handleGenerate3D}
        onRemoveBg={handleRemoveBg}
        loading={loading}
      />

      {/* Main canvas area */}
      <div style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>

        {/* View toggle tabs */}
        <div style={{
          position: 'absolute',
          top: '16px',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: '4px',
          background: '#fff',
          padding: '3px',
          borderRadius: '10px',
          border: '1px solid var(--border)',
          zIndex: 10,
          boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
        }}>
          {['2d', '3d'].map(v => (
            <button
              key={v}
              onClick={() => setActiveView(v)}
              style={{
                padding: '6px 18px',
                border: 'none',
                borderRadius: '7px',
                fontSize: '12px',
                fontWeight: '600',
                cursor: 'pointer',
                background: activeView === v ? '#1a1a1a' : 'transparent',
                color: activeView === v ? '#fff' : 'var(--muted)',
                transition: 'all 0.15s',
              }}
            >
              {v === '2d' ? '2D Canvas' : '3D Viewer'}
            </button>
          ))}
        </div>

        {/* Loading overlay */}
        {loading && (
          <div style={{
            position: 'absolute', inset: 0,
            background: 'rgba(248,248,246,0.7)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            zIndex: 20, backdropFilter: 'blur(4px)',
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{
                width: '36px', height: '36px',
                border: '3px solid var(--border)',
                borderTop: '3px solid var(--accent)',
                borderRadius: '50%',
                animation: 'spin 0.8s linear infinite',
                margin: '0 auto 12px',
              }} />
              <div style={{ fontSize: '13px', color: 'var(--muted)', fontWeight: '500' }}>
                {status}
              </div>
            </div>
          </div>
        )}

        {/* 2D Canvas */}
        {activeView === '2d' && (
          <Canvas2D imageBase64={imageBase64} onDownload={handleDownloadPNG} />
        )}

        {/* 3D Viewer */}
        {activeView === '3d' && modelUrl && (
          <Viewer3D modelUrl={modelUrl} onDownload={handleDownloadGLB} />
        )}

        {/* 3D empty state */}
        {activeView === '3d' && !modelUrl && (
          <div style={{
            width: '100%', height: '100%',
            display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center',
            gap: '12px', color: 'var(--muted)',
          }}>
            <div style={{
              width: '48px', height: '48px', borderRadius: '12px',
              background: 'var(--border)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '22px',
            }}>◈</div>
            <div style={{ fontSize: '14px', fontWeight: '500' }}>No 3D model yet</div>
            <div style={{ fontSize: '12px' }}>Switch to 3D mode and enter a prompt</div>
          </div>
        )}
      </div>

      {/* Status / error toast */}
      {!loading && <StatusBar status={status} error={error} />}

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}