import { useEffect, useRef } from 'react'
import { Event } from '../hooks/useSocket'

export default function ActivityLayer({ events }: { events: Event[] }) {
  const container = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (container.current) {
      container.current.scrollTop = container.current.scrollHeight
    }
  }, [events])
  
  return (
    <div style={{
      background: 'rgba(20,20,30,0.6)',
      backdropFilter: 'blur(12px)',
      borderRadius: 12,
      padding: 16,
      maxHeight: 300,
      overflowY: 'auto',
      fontFamily: 'monospace',
      fontSize: 13,
      color: '#c0c0c0'
    }} ref={container}>
      {events.map((e, i) => (
        <div key={i} style={{ marginBottom: 4 }}>
          <span style={{ color: e.type === 'user' ? '#fff' : '#8ab4f8' }}>
            [{e.agent || e.type}]
          </span>{' '}
          {e.content}
        </div>
      ))}
    </div>
  )
}