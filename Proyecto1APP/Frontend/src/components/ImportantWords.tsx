import { useState } from "react";
import "tippy.js/dist/tippy.css";
import "tippy.js/animations/scale.css";
import axios from "axios";
import ReactWordcloud from "react-wordcloud";

const ImportantWords = () => {
    const [words, setWords] = useState([{ text: " ", value: 10 }]);
    const a: [number, number] = [10, 60];
    const options = {
        fontSizes:  a,
        colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
        enableTooltip: true,
        deterministic: false,
        fontFamily: "Helvetica",
        fontStyle: "normal",
        fontWeight: "bold",
        padding: 1,
        rotations: 0,
        transitionDuration: 1000
    };

    const handleClick = async (classId: number) => {
        console.log("Fetching important words...");
        const myElement = document.getElementById("label" + classId.toString());
        if (myElement) {
            myElement.style.fontWeight = "bold";
        }
        for (let i = 1; i <= 5; i++) {
            if (i !== classId) {
                const myElement = document.getElementById("label" + i.toString());
                if (myElement) {
                    myElement.style.fontWeight = "normal";
                }
            }
        }
        try {
            const response = await axios.get(`http://127.0.0.1:8000/words/${classId}`);
            setWords(response.data);
            console.log("Words fetched successfully:", words);
        } catch (error) {
            console.error("Error fetching prediction:", error);
            alert("Failed to fetch prediction. Check the console for more details.");
        }
    };

    return (
        <div>
            <div>
			<h1 style={{fontWeight: "bold", justifyContent: "center", display: "flex"}}>Palabras más relevantes por Clase</h1>
                <div style={{ display: "flex", justifyContent: "center" }}>
                    <h3 id="label1" onClick={() => handleClick(1)}>Clase 1&nbsp;&nbsp;</h3>
                    <h3 id="label2" onClick={() => handleClick(2)}>Clase 2&nbsp;&nbsp;</h3>
                    <h3 id="label3" onClick={() => handleClick(3)}>Clase 3&nbsp;&nbsp;</h3>
                    <h3 id="label4" onClick={() => handleClick(4)}>Clase 4&nbsp;&nbsp;</h3>
                    <h3 id="label5" onClick={() => handleClick(5)}>Clase 5</h3>
                </div>
                <div id="cloud">
                    <ReactWordcloud options={options} words={words} />
                </div>
            </div>
        </div>
    );
};
export default ImportantWords;