import React,{ createContext, useEffect, useMemo, useState } from "react";

export const defaultUpdatedValue : UpdatedValue = {time:new Date().toLocaleTimeString(), WaterLevel:[0,0,0], MotorSpeed:[0,0]}
// Create a Context
export const UpdatedValueContext = createContext(defaultUpdatedValue);

export interface UpdatedValue {
    time: string,
    WaterLevel:number[], 
    MotorSpeed: number[],
}

export const UpdatedValueContextProvider = ({ children }) => {
    
    const [state, setState] = useState(defaultUpdatedValue);
  
    useEffect(() => {
        var valueOld : UpdatedValue = defaultUpdatedValue
        const eventSource = new EventSource('/event');  
        eventSource.onmessage = (event) => {
            // console.log(event)
            const data = JSON.parse(event.data)
            if(data !== valueOld) {
                valueOld = data;
                setState(data)
            }
        };  

        eventSource.onerror = () => {  

            console.error('SSE connection error');  

            eventSource.close();  

        };  

        return () => {  

            eventSource.close();  

        };  
    }, []);  


    // useMemo( () => {
    //     var valueOld : UpdatedValue = defaultUpdatedValue
    //     setInterval( function() {
    //         getUpdatedValue().then( (value) => { if(value !== valueOld) {
    //             valueOld = value;
    //             setState(value)
    //         } } );
    //     }, 1000 )
    //  }, [] )
  
    return (
      <UpdatedValueContext.Provider value={ state }>
        {children}
      </UpdatedValueContext.Provider>
    );
};

export async function getUpdatedValue() : Promise<UpdatedValue> {

    var value : UpdatedValue = defaultUpdatedValue

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
