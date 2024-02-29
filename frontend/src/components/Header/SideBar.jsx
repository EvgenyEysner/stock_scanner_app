import {useState} from 'react';
import Offcanvas from 'react-bootstrap/Offcanvas';
import {FaBarcode, FaBars, FaCartShopping, FaHouse} from "react-icons/fa6";
import Nav from 'react-bootstrap/Nav';
import {FaUser} from "react-icons/fa";

export const SideBar = () => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <FaBars size={48} color={"white"} onClick={handleShow}/>

      <Offcanvas show={show} onHide={handleClose}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menü</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <Nav defaultActiveKey="/home" className="flex-column">
            <Nav.Link href="/"><FaHouse size={24}/> Home</Nav.Link>
            <Nav.Link href="#link"><FaUser size={24}/> Benutzer</Nav.Link>
            <Nav.Link href="/scan"><FaBarcode size={24}/> Scanner</Nav.Link>
            <Nav.Link href="#link"><FaCartShopping size={24}/> Korb</Nav.Link>
          </Nav>
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
}
