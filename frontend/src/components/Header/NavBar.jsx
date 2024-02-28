import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import {FaBarcode, FaUser} from "react-icons/fa";
import {FaHelmetSafety} from "react-icons/fa6";

export const NavBar = () => {
  return (
    <>
      <Navbar expand="lg" data-bs-theme="dark" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="/"><FaHelmetSafety size={48}/></Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav"/>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="p-2 ms-auto">
              <Nav.Link href="#link"><FaUser size={24}/></Nav.Link>
              <Nav.Link href="/scan"><FaBarcode size={32}/> </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}
