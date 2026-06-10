import { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { Environment } from '@react-three/drei'
import HenryCore from '../components/HenryCore'
import ActivityLayer from '../components/ActivityLayer'
import CommandInput from '../components/CommandInput'
import { useSocket, Event } from '../hooks/useSocket'

export default function Home() {
  const [events, setEvents] = useState<Event[]>([])
  const { connect, sendMessage, lastEvent } = useSocket('ws://localhost:8000/ws/default')
  
  useEffect(() => {
    connect()
  }, [])
  
  useEffect(() => {
    if (lastEvent) setEvents(prev => [...prev, lastEvent])
  }, [lastEvent])

  const handleCommand = (text: string) => {
    sendMessage(text)
    setEvents(prev => [...prev, { type: 'user', content: text, agent: 'user' }])
  }

  return (
    <div style={{ position: 'relative', height: '100vh', overflow: 'hidden' }}>
      {/* 3D Core */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
        <Canvas camera={{ position: [0, 0, 3.5], fov: 45 }}>
          <Environment preset="city" />
          <HenryCore events={events} />
        </Canvas>
      </div>
      
      {/* Overlay UI */}
      <div style={{ position: 'absolute', top: 20, left: 20, right: 20, bottom: 20, zIndex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <ActivityLayer events={events} />
        <CommandInput onSend={handleCommand} />
      </div>
    </div>
  )
}