import { useState } from 'react'

const styles = {
  sidebar: {
    width: 'var(--sidebar)',
    minWidth: 'var(--sidebar)',
    height: '100%',
    background: 'var(--surface)',
    borderRight: '1px solid var(--border)',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  },
  header: {
    padding: '20px 20px 16px',
    borderBottom: '1px solid var(--border)',
  },
  logo: {
    fontSize: '15px',
    fontWeight: '600',
    letterSpacing: '-0.3px',
    color: 'var(--text)',
  },
  logoSub: {
    fontSize: '11px',
    color: 'var(--muted)',
    marginTop: '2px',
  },
  body: {
    flex: 1,
    overflowY: 'auto',
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  section: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  label: {
    fontSize: '11px',
    fontWeight: '600',
    color: 'var(--muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  textarea: {
    width: '100%',
    minHeight: '90px',
    padding: '10px 12px',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    background: 'var(--bg)',
    color: 'var(--text)',
    fontSize: '13px',
    resize: 'vertical',
    fontFamily: 'inherit',
    outline: 'none',
    lineHeight: '1.5',
  },
  select: {
    width: '100%',
    padding: '8px 12px',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    background: 'var(--bg)',
    color: 'var(--text)',
    fontSize: '13px',
    outline: 'none',
    cursor: 'pointer',
  },
  row: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '8px',
  },
  input: {
    width: '100%',
    padding: '8px 12px',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    background: 'var(--bg)',
    color: 'var(--text)',
    fontSize: '13px',
    outline: 'none',
  },
  divider: {
    height: '1px',
    background: 'var(--border)',
  },
  btnPrimary: {
    width: '100%',
    padding: '10px',
    background: 'var(--accent)',
    color: '#fff',
    border: 'none',
    borderRadius: 'var(--radius)',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background 0.15s',
  },
  btnSecondary: {
    width: '100%',
    padding: '10px',
    background: 'transparent',
    color: 'var(--text)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    fontSize: '13px',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'border-color 0.15s',
  },
  modeTab: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '4px',
    background: 'var(--bg)',
    padding: '3px',
    borderRadius: 'var(--radius)',
    border: '1px solid var(--border)',
  },
  tab: (active) => ({
    padding: '7px',
    border: 'none',
    borderRadius: '6px',
    fontSize: '12px',
    fontWeight: '500',
    cursor: 'pointer',
    background: active ? 'var(--surface)' : 'transparent',
    color: active ? 'var(--text)' : 'var(--muted)',
    boxShadow: active ? '0 1px 3px rgba(0,0,0,0.08)' : 'none',
    transition: 'all 0.15s',
  }),
}

export default function Sidebar({ onGenerate2D, onGenerate3D, onRemoveBg, loading }) {
  const [mode, setMode] = useState('2d')
  const [prompt, setPrompt] = useState('')
  const [model, setModel] = useState('flux')
  const [width, setWidth] = useState(1024)
  const [height, setHeight] = useState(1024)

  const handle2D = () => {
    if (!prompt.trim()) return
    onGenerate2D({ prompt, model, width, height })
  }

  const handle3D = () => {
    if (!prompt.trim()) return
    onGenerate3D({ prompt })
  }

  return (
    <div style={styles.sidebar}>
      <div style={styles.header}>
        <div style={styles.logo}>Generative Studio</div>
        <div style={styles.logoSub}>API-powered · Free tier</div>
      </div>

      <div style={styles.body}>

        {/* Mode toggle */}
        <div style={styles.section}>
          <div style={styles.label}>Mode</div>
          <div style={styles.modeTab}>
            <button style={styles.tab(mode === '2d')} onClick={() => setMode('2d')}>2D Image</button>
            <button style={styles.tab(mode === '3d')} onClick={() => setMode('3d')}>3D Model</button>
          </div>
        </div>

        {/* Prompt */}
        <div style={styles.section}>
          <div style={styles.label}>Prompt</div>
          <textarea
            style={styles.textarea}
            placeholder={mode === '2d'
              ? 'A ceramic mug on a marble surface...'
              : 'A sleek sports car, centered, white bg...'}
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
          />
        </div>

        {/* 2D options */}
        {mode === '2d' && (
          <>
            <div style={styles.section}>
              <div style={styles.label}>Model</div>
              <select style={styles.select} value={model} onChange={e => setModel(e.target.value)}>
                <option value="flux">FLUX (best quality)</option>
                <option value="turbo">Turbo (faster)</option>
              </select>
            </div>

            <div style={styles.section}>
              <div style={styles.label}>Resolution</div>
              <div style={styles.row}>
                <div>
                  <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: 4 }}>Width</div>
                  <input
                    style={styles.input}
                    type="number"
                    value={width}
                    onChange={e => setWidth(Number(e.target.value))}
                    step={64} min={256} max={1024}
                  />
                </div>
                <div>
                  <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: 4 }}>Height</div>
                  <input
                    style={styles.input}
                    type="number"
                    value={height}
                    onChange={e => setHeight(Number(e.target.value))}
                    step={64} min={256} max={1024}
                  />
                </div>
              </div>
            </div>

            <div style={styles.divider} />

            <div style={styles.section}>
              <button
                style={styles.btnPrimary}
                onClick={handle2D}
                disabled={loading}
              >
                {loading ? 'Generating...' : 'Generate Image'}
              </button>
              <button
                style={styles.btnSecondary}
                onClick={onRemoveBg}
                disabled={loading}
              >
                Remove Background
              </button>
            </div>
          </>
        )}

        {/* 3D options */}
        {mode === '3d' && (
          <>
            <div style={{ fontSize: '12px', color: 'var(--muted)', lineHeight: '1.5' }}>
              Text → 2D image → 3D model (.GLB) pipeline.
              Best results with centered objects on white backgrounds.
            </div>
            <div style={styles.divider} />
            <div style={styles.section}>
              <button
                style={styles.btnPrimary}
                onClick={handle3D}
                disabled={loading}
              >
                {loading ? 'Generating 3D...' : 'Generate 3D Model'}
              </button>
            </div>
          </>
        )}

      </div>
    </div>
  )
}