import React,{ createContext, useMemo, useState } from "react";

// Create a Context
export const MotorSpeedContext = createContext([0, 0, 0]);

export const MotorSpeedContextProvider = ({ children }) => {
    
    const [state, setState] = useState([0, 0, 0]);

    useMemo( () => {
        var valueOld : number[] = [0, 0, 0]
        setInterval( function() {
            getMotorSpeed().then( (value) => { if(value !== valueOld) {
                valueOld = value;
                setState(value)
            } } );
        }, 1000 )
     }, [] )
  
    return (
      <MotorSpeedContext.Provider value={ state }>
        {children}
      </MotorSpeedContext.Provider>
    );
};

export async function getMotorSpeed() : Promise<number[]> {

    var value : number[] = []

    try {
        const response = await fetch('/GetMotorSpeed');
        if (!response.ok) {
            throw new Error(`Bad server response : ${response.statusText}`);
        }
        const data : number[] = await response.json();
        value = data;
    } catch (error) {
        throw new Error("Something went wrong in getMotorSpeed().")
    }

    return value
};
