import { useState } from 'react'
import './App.css'
import Inicio from './Inicio/Inicio'
import videobg from './assets/media/background-video.mp4';

function App() {
  return (
    <>
      <video className='videobg' src={videobg} autoPlay loop muted />
      <Inicio />
    </>
  )
}

export default App
