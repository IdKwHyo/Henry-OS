import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { MeshDistortMaterial, Float } from '@react-three/drei'
import * as THREE from 'three'
import { Event } from '../hooks/useSocket'
import gsap from 'gsap'

export default function HenryCore({ events }: { events: Event[] }) {
  const mesh = useRef<THREE.Mesh>()
  const material = useRef<any>()
  
  useFrame((state) => {
    if (mesh.current) {
      mesh.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.2
      mesh.current.rotation.y += 0.001
      mesh.current.rotation.z += 0.0005
    }
  })
  
  // React to latest event for state change (simplified)
  useEffect(() => {
    if (events.length === 0) return
    const last = events[events.length - 1]
    if (last.type === 'thinking') {
      gsap.to(material.current, { distort: 0.5, duration: 0.5 })
    } else if (last.type === 'response') {
      gsap.to(material.current, { distort: 0.1, duration: 1 })
    }
  }, [events])
  
  return (
    <Float speed={1.5} rotationIntensity={0.3} floatIntensity={0.5}>
      <mesh ref={mesh} position={[0, 0, 0]}>
        <sphereGeometry args={[1, 128, 128]} />
        <MeshDistortMaterial
          ref={material}
          color="#7c8a9a"
          roughness={0.1}
          metalness={0.8}
          clearcoat={1}
          clearcoatRoughness={0.1}
          distort={0.1}
          speed={2}
        />
      </mesh>
    </Float>
  )
}