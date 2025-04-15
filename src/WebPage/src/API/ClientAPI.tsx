import React,{ createContext, useEffect, useState } from "react";
import { GetData } from "./GetData.tsx";
import { PostData } from "./PostData.tsx";

export const defaultUpdatedClientData : UpdatedClientData = {ClientEnabled: false, ActiveClients:{Ip: "", Name: "", lastPing: 0}, ClientList:[]}
// Create a Context
export const UpdatedClientDataContext = createContext(defaultUpdatedClientData);

export interface Client {
    Ip : string
    Name : string
    lastPing : number
}

export interface UpdatedClientData {
    ClientEnabled : boolean,
    ActiveClients: Client,
    ClientList: Client[],
}

export const UpdatedClientDataContextProvider = ({ children }) => {

    const [state, setState] = useState(defaultUpdatedClientData);

    useEffect(() => {
        var valueOld : UpdatedClientData = defaultUpdatedClientData

        GetData<UpdatedClientData>('/GetClientsData').then((data) => { console.log(data); valueOld = data; setState(data)})

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

export const ChangeClientMode = async (value : boolean) => {
    PostData('/ChangeClientMode', { ClientEnabled: value })
}