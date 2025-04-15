import React, { JSX } from "react"
import './ClientPanel.css';
import { Client } from "../../API/ClientAPI";

export interface ClientPanelProps {
    client: Client
}

export const ClientPanel = ( {client} : ClientPanelProps ) : JSX.Element => {
    
    return (
        <div className="ClientPanel">
            <h1>{client.Name}</h1>
            <p>{client.Ip}</p>
        </div>
    )
}