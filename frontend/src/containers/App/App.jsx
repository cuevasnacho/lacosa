import './App.css'
import UnirsePartida from "../../components/UnirsePartida/UnirsePartida.jsx"
import {BrowserRouter as Router,Routes,Route} from "react-router-dom"


function App() {
  
  return (
    <>
    <Router>
      <Routes>
          <Route exact path="/UnirsePartida" element={<UnirsePartida/>}></Route>
      </Routes>
    </Router>
    </>
  )
}
export default App
