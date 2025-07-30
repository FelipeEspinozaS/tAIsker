import ClerkProviderWithRoutes from './auth/ClerkProviderWithRoutes.tsx'
import { Routes, Route } from 'react-router-dom'
import { AuthenticationPage } from './auth/AuthenticationPage.tsx'
import './App.css'

function App() {

  return (
    <ClerkProviderWithRoutes>
      <Routes>
        <Route path="/signin/*" element={<AuthenticationPage />} />
        <Route path="/signup" element={<AuthenticationPage />} />
      </Routes>
    </ClerkProviderWithRoutes> 
  )
}

export default App
