import { useState, useRef } from 'react'

export interface Event {
  type: string
  content: string
  agent?: string
}

export const useSocket = (url: string) => {
  const [lastEvent, setLastEvent] = useState<Event | null>(null)
  const ws = useRef<WebSocket | null>(null)
  
  const connect = () => {
    ws.current = new WebSocket(url)
    ws.current.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data)
        setLastEvent(data)
      } catch {}
    }
  }
  
  const sendMessage = (text: string) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(text)
    }
  }
  
  return { connect, sendMessage, lastEvent }
}