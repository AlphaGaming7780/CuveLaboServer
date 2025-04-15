import React, { JSX } from "react"
import './ClientPanel.css';
import { Client } from "../../API/ClientAPI";

export interface ClientPanelProps {
    client: Client
    index?: number
}

export const ClientPanel = ( {client, index = -1} : ClientPanelProps ) : JSX.Element => {
    
    if(!client) {
        return <div className="ClientPanel">No client data available</div>;
    }

    return (
        <div className="ClientPanel" style={{flexDirection: index >= 0 ? "row" : "column"}}>
            {
                index >= 0 ? <>
                    <h1 style={{paddingRight:"10px"}}>{index}</h1>
                    <div>
                        <h3>{client.Name}</h3>
                        <p>{client.Ip}</p>
                    </div>
                </> : 
                <>
                    <h3>{client.Name}</h3>
                    <p>{client.Ip}</p>
                </>
            }

        </div>
    )
}