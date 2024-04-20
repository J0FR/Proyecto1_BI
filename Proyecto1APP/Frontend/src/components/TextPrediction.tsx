import React, { useState } from "react";
import { Button, Form, Container } from "react-bootstrap";
import axios from "axios";

const TextPrediction = () => {
	const [input, setInput] = useState("");
	const [prediction, setPrediction] = useState<number | null>(null);
	const [score, setScore] = useState<number | null>(null);


	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		const postData = {
			'Review': input,
		};
		try {
			const response = await axios.post(
				"http://127.0.0.1:8000/predict",
				postData
			);
			setPrediction(response.data.predictions[0]);
			setScore((response.data.score).toFixed(2));
		} catch (error) {
			console.error("Error fetching prediction:", error);
			alert("Failed to fetch prediction. Check the console for more details.");
		}
	};

	return (
		<Container style={{ maxWidth: "500px", margin: "20px auto" }}>
			<h1 style={{ textAlign: "center", fontWeight: "bold"}}>Predicción por Texto</h1>
			<Form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
				<Form.Group controlId="formText">
					<Form.Control
						as="textarea"
						placeholder="Ingrese texto..."
						rows={5}
						value={input}
						onChange={(e) => setInput(e.target.value)}
						style={{ marginBottom: "20px" }}
					/>
				</Form.Group>
				<Button variant="primary" type="submit" size="lg" className="w-100">
					Enviar
				</Button>
			</Form>
			<br />
			<div style={{ display: 'flex', justifyContent: 'center', textAlign: 'center'}}>
				<div style={{ display: 'table-column', justifyContent: 'center', textAlign: 'center'}} >
					<h2 style={{ textAlign: "center",  minWidth: '150px'}}>Predicción</h2>
					<div
						style={{
							backgroundColor: "#f8f9fa",
							minHeight: "60px",
							display: "grid",
							justifyContent: "center",
							alignItems: "center",
							fontSize: "24px",
							borderRadius: "5px",
						}}
						>
						{prediction !== null ? prediction : ""}
					</div>
				</div>

				<div>
					<h1>&nbsp;&nbsp;</h1>
				</div>

				<div style={{ display: 'table-column'}} >
					<h2 style={{ textAlign: "center",  minWidth: '150px'}}>Score</h2>
					<div
						style={{
							backgroundColor: "#f8f9fa",
							minHeight: "60px",
							display: "grid",
							justifyContent: "center",
							alignItems: "center",
							fontSize: "24px",
							borderRadius: "5px",
						}}
						>
						{score !== null ? score : ""}
					</div>
				</div>
			</div>
		</Container>
	);
};

export default TextPrediction;
