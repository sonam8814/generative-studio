export default function StatusBar({ status, error }) {
  if (!status && !error) return null

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      left: '50%',
      transform: 'translateX(-50%)',
      padding: '10px 20px',
      borderRadius: '20px',
      fontSize: '13px',
      fontWeight: '500',
      background: error ? '#fee2e2' : '#1a1a1a',
      color: error ? '#991b1b' : '#fff',
      boxShadow: '0 4px 16px rgba(0,0,0,0.12)',
      zIndex: 100,
      maxWidth: '400px',
      textAlign: 'center',
      transition: 'all 0.2s',
    }}>
      {error || status}
    </div>
  )
}