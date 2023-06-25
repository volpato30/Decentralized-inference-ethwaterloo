import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import {LinkContainer} from 'react-router-bootstrap';
import logo from "../../assets/logo.png";

function NavBar() {
  return (
    <Navbar bg="light" expand="lg">
      <Container>
      <LinkContainer to="/">
        <Navbar.Brand>
          <img
              alt=""
              src={logo}
              width="50"
              height="30"
              className="d-inline-block align-top"
          />{'  '}DI protocol</Navbar.Brand>
      </LinkContainer>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <LinkContainer to="/stake">
              <Nav.Link>Stake</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/unstake">
              <Nav.Link>Unstake</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/modelRegistry">
              <Nav.Link>Register Model</Nav.Link>
            </LinkContainer>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;