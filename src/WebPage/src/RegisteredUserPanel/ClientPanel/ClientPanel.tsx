import React, { JSX } from "react"
import './ClientPanel.css';
import { Client } from "../../API/ClientAPI";

export interface ClientPanelProps {
    client: Client
}

export const ClientPanel = ( {client} : ClientPanelProps ) : JSX.Element => {
    
    if(!client) {
        return <div className="ClientPanel">No client data available</div>;
    }

    return (
        <div className="ClientPanel">
            <h3>{client.Name}</h3>
            <p>{client.Ip}</p>
        </div>
    )
}