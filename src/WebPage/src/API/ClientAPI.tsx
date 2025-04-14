import React,{ createContext, useEffect, useState } from "react";
import { GetData } from "./GetData.tsx";

export const defaultUpdatedClientData : UpdatedClientData = {ActiveClients:"null", ClientList:[]}
// Create a Context
export const UpdatedClientDataContext = createContext(defaultUpdatedClientData);

export interface Client {
    Ip : string
    Name : string
    lastPing : number
}

export interface UpdatedClientData {
    ActiveClients: string,
    ClientList: Client[],
}

export const UpdatedClientDataContextProvider = async ({ children }) => {

    const [state, setState] = useState(defaultUpdatedClientData);

    GetData<UpdatedClientData>('/GetClientsData').then((data) => { console.log(data); setState(data)})

    useEffect(() => {
        var valueOld : UpdatedClientData = defaultUpdatedClientData
        const eventSource = new EventSource('/ClientsDataUpdate');  
        eventSource.onmessage = (event) => {
            // console.log(event)
            const data = JSON.parse(event.data)
            if(data !== valueOld) {
                valueOld = data;
                console.log(data)
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
  
    return (
      <UpdatedClientDataContext.Provider value={ state }>
        {children}
      </UpdatedClientDataContext.Provider>
    );
};

export const ResetActiveClient = async () => {
    const response = await fetch('/ResetActiveClient', { method: 'POST' });
    if (!response.ok) {
        throw new Error(`Bad server response : ${response.statusText}`);
    }
}