import React, { useContext } from 'react';
import './RegisteredUserPanel.css';
import { ChangeClientMode, ResetActiveClient, UpdatedClientDataContext } from '../API/ClientAPI.tsx';
import { RadioCheckbox } from './RadioCheckbox/RadioCheckbox.tsx';

export const RegisteredUserPanel = () => {

    const { ClientEnabled, ActiveClients, ClientList } = useContext(UpdatedClientDataContext)

    return (
        <div className="registered-user-panel">
            <h2>Registered User Panel</h2>
            <p>This is the registered user panel.</p>
            <button type='button' onClick={ () => ResetActiveClient() } >Reset Active Client</button>
            <span style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
                <RadioCheckbox checked={ClientEnabled} onChange={ChangeClientMode} />
                <p style={{paddingLeft: "0.4rem" }}>Disable/Enable</p>
            </span>
        </div>
    );
}
