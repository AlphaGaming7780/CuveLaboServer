import React,{ createContext, useState } from "react";

export const defaultBaseData : BaseData = { numberOfCuve:0, numberOfMotor: 0 }
// Create a Context
export const BaseDataContext = createContext(defaultBaseData);

export interface BaseData {
    numberOfCuve: number,
    numberOfMotor: number
}

export const BaseDataContextProvider = async ({ children }) => {
    
    const [state, setState] = useState(defaultBaseData);
  
    let data : BaseData = defaultBaseData;

    while(data === defaultBaseData || data === undefined) {
        try {
            const response = await fetch('/GetBaseData');
    
            console.log(response)

            // request.then( async (response) => {
            if(!response.ok) return;
    
            const json = await response.json();
    
            data = JSON.parse(json);
                
            // })
        } catch (error) {
            console.error(error.message);
        }
    }

    setState(data);
  
    return (
      <BaseDataContext.Provider value={ state }>
        {children}
      </BaseDataContext.Provider>
    );
};
