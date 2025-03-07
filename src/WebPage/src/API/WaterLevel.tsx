import React,{ createContext, useMemo, useState } from "react";

// Create a Context
export const WaterLevelContext = createContext([0, 0, 0]);

export const WaterLevelContextProvider = ({ children }) => {
    
    const [state, setState] = useState([0, 0, 0]);

    useMemo( () => {
        var valueOld : number[] = [0, 0, 0]
        setInterval( function() {
            getWaterLevel().then( (value) => { if(value !== valueOld) {
                valueOld = value;
                setState(value)
            } } );
        }, 1000 )
     }, [] )
  
    return (
      <WaterLevelContext.Provider value={ state }>
        {children}
      </WaterLevelContext.Provider>
    );
};

export async function getWaterLevel() : Promise<number[]> {

    var value : number[] = []

    try {
        const response = await fetch('/GetWaterLevel');
        if (!response.ok) {
            throw new Error(`Bad server response : ${response.statusText}`);
        }
        const data : number[] = await response.json();
        value = data;
    } catch (error) {
        throw new Error("Something went wrong in getWaterLevel().")
    }

    return value
};
