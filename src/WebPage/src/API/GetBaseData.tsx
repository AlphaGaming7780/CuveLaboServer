import React,{ createContext, useEffect, useState } from "react";

export const defaultBaseData : BaseData = { numberOfCuve:0, numberOfMotor: 0 }
// Create a Context
export const BaseDataContext = createContext(defaultBaseData);

export interface BaseData {
    numberOfCuve: number,
    numberOfMotor: number
}

export const BaseDataContextProvider = ({ children }) => {
    const [state, setState] = useState<BaseData>(defaultBaseData);
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('/GetBaseData');
          if (!response.ok) {
            console.error("Erreur de réponse serveur :", response.status);
            return;
          }
  
          const data = await response.json();
          setState(data);
        } catch (error) {
          console.error("Erreur lors du fetch de base data:", error.message);
        }
      };
  
      // Lancer le fetch seulement si on est à l’état par défaut
      if (state === defaultBaseData) {
        fetchData();
      }
  
    }, [state]);
  
    return (
      <BaseDataContext.Provider value={state}>
        {children}
      </BaseDataContext.Provider>
    );
  };
