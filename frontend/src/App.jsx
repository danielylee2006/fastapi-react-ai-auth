import { useState } from 'react'
import './App.css'
import {Routes, Route} from "react-router-dom"
import {ClerkProviderWithRoutes} from "./auth/ClerkProviderWithRoutes.jsx"

function App() {
  return <ClerkProviderWithRoutes>
  
  <Routes>
    
  </Routes>

  </ClerkProviderWithRoutes>
}

export default App
