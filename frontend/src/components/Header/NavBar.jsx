import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import {SideBar} from "./SideBar";
import {FaHelmetSafety} from "react-icons/fa6";

export const NavBar = () => {
  return (
    <>
      <Navbar expand="lg" data-bs-theme="dark" className="bg-body-tertiary">
        <Container>
          <SideBar/>
          <Navbar.Brand href="/"><FaHelmetSafety size={48}/></Navbar.Brand>
        </Container>
      </Navbar>
    </>
  )
}
