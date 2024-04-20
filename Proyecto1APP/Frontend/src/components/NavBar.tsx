import { Navbar, Nav } from "react-bootstrap";
import "./NavBar.css"; // Import custom CSS file

const NavBar = () => {
	return (
		<>
			<Navbar bg="light" expand="lg">
				<Navbar.Toggle aria-controls="basic-navbar-nav" />
				<Navbar.Collapse id="basic-navbar-nav">
					<Nav className="mx-auto nav">
						{" "}
						{}
						<Nav.Link href="/text">Predicción por Texto</Nav.Link>
						<span className="separator">|</span> {}
						<Nav.Link href="/csv">Predicción CSV</Nav.Link>
					</Nav>
				</Navbar.Collapse>
			</Navbar>
			<br />
		</>
	);
};

export default NavBar;
