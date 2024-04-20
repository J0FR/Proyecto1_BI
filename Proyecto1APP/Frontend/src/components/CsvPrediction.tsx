import React, { useState } from "react";
import { Button, Form, Container } from "react-bootstrap";
import axios from "axios";

const CsvPrediction = () => {
	const [file, setFile] = useState<File | null>(null);
	const [isUploading, setIsUploading] = useState(false);
	const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

	const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setFile(e.target.files ? e.target.files[0] : null);
		setDownloadUrl(null); // Reset download URL when file is changed
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (file) {
			setIsUploading(true);
			const formData = new FormData();
			formData.append("file", file);

			try {
				const response = await axios.post(
					"http://127.0.0.1:8000/upload2",
					formData,
					{
						headers: {
							"Content-Type": "multipart/form-data",
						},
						responseType: "blob", // Important: specify responseType
					}
				);
				const url = window.URL.createObjectURL(new Blob([response.data]));
				setDownloadUrl(url);
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
			<h1 style={{fontWeight: "bold"}}>Predicción CSV</h1>
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
			<h4 className="mt-4">Descargar predicción...</h4>
			{downloadUrl ? (
				<a
					href={downloadUrl}
					download={`predictions_${file?.name}`}
					className="btn btn-success mt-3"
				>
					Descargar
				</a>
			) : (
				<Button variant="danger" className="mt-3" disabled>
					Descargar
				</Button>
			)}
		</Container>
	);
};

export default CsvPrediction;
