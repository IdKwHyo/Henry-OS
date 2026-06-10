import { useState } from 'react'

export default function CommandInput({ onSend }: { onSend: (text: string) => void }) {
  const [text, setText] = useState('')
  
  const submit = () => {
    if (text.trim()) {
      onSend(text.trim())
      setText('')
    }
  }
  
  return (
    <div style={{ display: 'flex', gap: 8 }}>
      <input
        type="text"
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && submit()}
        placeholder="Command Henry..."
        style={{
          flex: 1,
          background: 'rgba(30,30,40,0.8)',
          border: '1px solid #3a3a4a',
          borderRadius: 8,
          padding: 12,
          color: '#fff',
          backdropFilter: 'blur(8px)'
        }}
      />
      <button onClick={submit} style={{
        background: '#2a2a3a',
        border: 'none',
        borderRadius: 8,
        padding: '0 20px',
        color: '#e0e0e0',
        cursor: 'pointer'
      }}>Send</button>
    </div>
  )
}