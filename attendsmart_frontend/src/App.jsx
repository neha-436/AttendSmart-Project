// import Login from "./pages/Login"

// function App() {
//   return (
//     <div>
//       <h1>AttendSmart</h1>
//       <Login />
//     </div>
//   )
// }

// export default App

import { Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  )
}

export default App