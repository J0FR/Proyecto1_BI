import React, { useState } from "react";
import { Button, Form, Container } from "react-bootstrap";
import axios from "axios";

const Model = () => {
    const [f1, setF1] = useState(0);
    const [recall, setRecall] = useState(0);
    const [precision, setPrecision] = useState(0);
    
    const handleClick = async () => {
        try {
            const metrics = await axios.get(`http://127.0.0.1:8000/report`);
            const obj = metrics.data;
            console.log(obj);
            setF1(obj.f1);
            setRecall(obj.recall);
            setPrecision(obj.precision);    
        } catch (error) {
            console.error("Error fetching prediction:", error);
            alert("Failed to fetch prediction. Check the console for more details.");
        }
    };
    handleClick()
	const [file, setFile] = useState<File | null>(null);
	const [isUploading, setIsUploading] = useState(false);

	const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setFile(e.target.files ? e.target.files[0] : null);
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (file) {
			setIsUploading(true);
			const formData = new FormData();
			formData.append("file", file);

			try {
                axios.post(
					"http://127.0.0.1:8000/upload2",
					formData,
					{
						headers: {
							"Content-Type": "multipart/form-data",
						},
						responseType: "blob", // Important: specify responseType
					}
				);
				setIsUploading(false);
			} catch (error) {
				console.error("Error uploading file:", error);
				setIsUploading(false);
			}
		}
	};

	return (

		<Container
        style={{ maxWidth: "500px", margin: "0 auto", textAlign: "center" }}
		>
            <div>
                <h1>Métricas del modelo</h1>
                <div>
                    <h3>Precisión: {precision}</h3>
                    <h3>Recall: {recall}</h3>
                    <h3>Puntaje F1: {f1}</h3>
                </div>                
            </div>
            <div>
                <h1>&nbsp;&nbsp;</h1>
            </div>
			<h1>Reentrenar modelo</h1>
			<h4>Cargar archivo CSV...</h4>
			<Form onSubmit={handleSubmit}>
				<Form.Group controlId="formFile" className="mb-3">
					<Form.Control type="file" onChange={handleFileChange} />
				</Form.Group>
				<Button
					variant={isUploading ? "danger" : "success"}
					type="submit"
					disabled={!file || isUploading}
				>
					{isUploading ? "Cargando..." : "Enviar"}
				</Button>
			</Form>
		</Container>
	);
};

export default Model;
