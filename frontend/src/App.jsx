import { Navigate, Route, Routes } from 'react-router'
import './App.css'
import { Main } from './pages/Main'
import { Result } from './pages/Result'
import { Scanner } from './pages/Scanner'
import {NavBar} from "./components/Header/NavBar";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Page} from "./pages/Page";
import {Footer} from "./components/Footer/Footer";

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('./serviceworker.js')
      .then((reg) => console.log('Successfully registered: ', reg.scope))
      .catch((err) => console.log('Error registering: ', err))
  })
}

function App() {
  return (
    <>
      <NavBar/>
      <Page/>
      <Footer/>
    </>
  )
}

export default App
