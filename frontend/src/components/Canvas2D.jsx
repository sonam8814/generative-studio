const styles = {
  wrapper: {
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
    background: 'var(--bg)',
  },
  img: {
    maxWidth: '90%',
    maxHeight: '90%',
    borderRadius: '12px',
    boxShadow: '0 4px 24px rgba(0,0,0,0.08)',
    objectFit: 'contain',
  },
  placeholder: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '12px',
    color: 'var(--muted)',
  },
  icon: {
    width: '48px',
    height: '48px',
    borderRadius: '12px',
    background: 'var(--border)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '22px',
  },
  downloadBtn: {
    position: 'absolute',
    bottom: '16px',
    right: '16px',
    padding: '8px 16px',
    background: '#1a1a1a',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
  },
}

export default function Canvas2D({ imageBase64, onDownload }) {
  if (!imageBase64) {
    return (
      <div style={styles.wrapper}>
        <div style={styles.placeholder}>
          <div style={styles.icon}>✦</div>
          <div style={{ fontSize: '14px', fontWeight: '500' }}>No image yet</div>
          <div style={{ fontSize: '12px' }}>Enter a prompt and click Generate</div>
        </div>
      </div>
    )
  }

  return (
    <div style={styles.wrapper}>
      <img
        src={`data:image/png;base64,${imageBase64}`}
        alt="Generated"
        style={styles.img}
      />
      <button style={styles.downloadBtn} onClick={onDownload}>
        Download PNG
      </button>
    </div>
  )
}