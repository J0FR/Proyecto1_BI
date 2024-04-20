import React, { useState } from "react";
import { Button, Form, Container } from "react-bootstrap";
import axios from "axios";

const TextPrediction = () => {
	const [input, setInput] = useState("");
	const [prediction, setPrediction] = useState<number | null>(null);

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
		} catch (error) {
			console.error("Error fetching prediction:", error);
			alert("Failed to fetch prediction. Check the console for more details.");
		}
	};

	return (
		<Container style={{ maxWidth: "500px", margin: "20px auto" }}>
			<h1 style={{ textAlign: "center" }}>Predicción por Texto</h1>
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
			<h2 style={{ textAlign: "center" }}>Predicción:</h2>
			<div
				style={{
					backgroundColor: "#f8f9fa",
					minHeight: "60px",
					display: "flex",
					justifyContent: "center",
					alignItems: "center",
					fontSize: "24px",
					borderRadius: "5px",
				}}
			>
				{prediction !== null ? prediction : ""}
			</div>
		</Container>
	);
};

export default TextPrediction;
