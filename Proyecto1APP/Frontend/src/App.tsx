import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import NavBar from "./components/NavBar";
import TextPrediction from "./components/TextPrediction";
import CsvPrediction from "./components/CsvPrediction";

const App = () => {
	return (
		<Router>
			<div>
				<NavBar />
				<Routes>
					<Route path="/text" element={<TextPrediction />} />
					<Route path="/csv" element={<CsvPrediction />} />
					<Route path="/" element={<TextPrediction />} />
				</Routes>
			</div>
		</Router>
	);
};

export default App;
