import React, { useMemo } from "react";
import "./Wave.css"

// https://codepen.io/goodkatz/pen/LYPGxQz?editors=1100
export function Wave() : React.JSX.Element {
    return (
        <svg className="waves" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 24 150 28" preserveAspectRatio="none" shape-rendering="auto">
            <defs>
            <   path id="gentle-wave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" />
            </defs>
            <g className="parallax">
                <use xlinkHref="#gentle-wave" x="48" y="0" fill="rgba(0, 132, 255, 0.7)" style={{animationDelay:`${Math.random() * -5}s`}} />
                <use xlinkHref="#gentle-wave" x="48" y="3" fill="rgba(0, 132, 255, 0.5)" style={{animationDelay:`${Math.random() * -5}s`}}/>
                <use xlinkHref="#gentle-wave" x="48" y="5" fill="rgba(0, 132, 255, 0.3)" style={{animationDelay:`${Math.random() * -5}s`}}/>
                <use xlinkHref="#gentle-wave" x="48" y="7" fill="rgba(0, 132, 255,   1)" style={{animationDelay:`${Math.random() * -5}s`}}/>
            </g>
        </svg>
    )
}

function getWaterLevel( {waterLevel, waveMaxHeight = 0.1} : WaveWithLevelProps) {
    var WaveHeight = 0
    var SeaHeight = 0

    if(waterLevel < waveMaxHeight / 2) {
        WaveHeight = waterLevel * 2 * 100
        SeaHeight = 0;
    } else if (waterLevel > 1 - waveMaxHeight / 2) {
        WaveHeight = (1 - waterLevel) * 2 * 100
        SeaHeight = 100
    } else {
        WaveHeight = waveMaxHeight * 100
        SeaHeight = waterLevel * 100 - ( waveMaxHeight / 2 * 100 )
    }

    return { WaveHeight, SeaHeight }
}

export interface WaveWithLevelProps {
    waterLevel : number;
    waveMaxHeight? : number;
}

export function WaveWithLevel( waveWithLevelProps : WaveWithLevelProps ) : React.JSX.Element {

    const wave = useMemo( () => <Wave/>, [] )

    const {WaveHeight, SeaHeight} = getWaterLevel(waveWithLevelProps)

    return (
        <div className="waveWithLevel">
            <div className="wave-container" style={{height:`${WaveHeight}%`}}>
                {wave}
            </div>
            <div className="sea" style={{backgroundColor:"rgba(0, 132, 255, 1)", height:`${SeaHeight}%`, width:"100%"} } />     
        </div>
    )
}