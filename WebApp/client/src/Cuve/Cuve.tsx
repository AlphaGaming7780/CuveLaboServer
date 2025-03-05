import React, {useEffect, useState} from "react";
import "./Cuve.css"
import { Wave } from "../Wave/Wave.tsx";

export function Cuve() : React.JSX.Element {

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
