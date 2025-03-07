import React,{ createContext, useMemo, useState } from "react";

export const defaultUpdatedValue : UpdatedValue = {WaterLevel:[0,0,0], MotorSpeed:[0,0]}
// Create a Context
export const UpdatedValueContext = createContext(defaultUpdatedValue);

export interface UpdatedValue {
    WaterLevel:number[], 
    MotorSpeed: number[],
}

export const UpdatedValueContextProvider = ({ children }) => {
    
    const [state, setState] = useState(defaultUpdatedValue);

    useMemo( () => {
        var valueOld : UpdatedValue = defaultUpdatedValue
        setInterval( function() {
            getUpdatedValue().then( (value) => { if(value !== valueOld) {
                valueOld = value;
                setState(value)
            } } );
        }, 1000 )
     }, [] )
  
    return (
      <UpdatedValueContext.Provider value={ state }>
        {children}
      </UpdatedValueContext.Provider>
    );
};

export async function getUpdatedValue() : Promise<UpdatedValue> {

    var value : UpdatedValue = {WaterLevel:[0,0,0], MotorSpeed:[0,0]}

    try {
        const response = await fetch('/GetUpdatedValue');
        if (!response.ok) {
            throw new Error(`Bad server response : ${response.statusText}`);
        }
        const data : UpdatedValue = await response.json();
        value = data;
    } catch (error) {
        throw new Error("Something went wrong in getUpdatedValue().")
    }

    return value
};
