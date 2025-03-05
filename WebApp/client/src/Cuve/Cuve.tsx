import React, {useEffect, useState} from "react";
import "./Cuve.css"
import { Wave } from "../Wave/Wave.tsx";

export function Cuve() : React.JSX.Element {

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
  
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/data');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setData(data);
                setLoading(false);
                } catch (error) {
                setError(error);
                setLoading(false);
            }
        };
  
      fetchData();
    }, []);

    return (
        <div className="cuve">

            <div className="cylindre-container" >
                <div className="cylindre" >
                    <div style={{height:"10%"}}>
                        <Wave/>
                    </div>
                    <div style={{backgroundColor:"rgba(0, 132, 255, 1)", height:"20%", width:"100%"} } />
                </div>
                <div className="cylindre" >
                    <div style={{height:"10%"}}>
                        <Wave/>
                    </div>
                    <div style={{backgroundColor:"rgba(0, 132, 255, 1)", height:"50%", width:"100%"} } />
                </div>
                <div className="cylindre" >
                    <div style={{height:"10%"}}>
                        <Wave/>
                    </div>
                    <div style={{backgroundColor:"rgba(0, 132, 255, 1)", height:"70%", width:"100%"} } />
                </div>
            </div>

            <div className="tank">
                <div className="wave-container">
                    <Wave/>
                </div>
            </div>

        </div>
    )
}
