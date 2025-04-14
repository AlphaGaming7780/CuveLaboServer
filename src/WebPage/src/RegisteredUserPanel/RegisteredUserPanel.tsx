import React from 'react';
import './RegisteredUserPanel.css';
import { ResetActiveClient } from '../API/ClientAPI.tsx';
import { RadioCheckbox } from './RadioCheckbox/RadioCheckbox.tsx';

export const RegisteredUserPanel = () => {

    return (
        <div className="registered-user-panel">
            <h2>Registered User Panel</h2>
            <p>This is the registered user panel.</p>
            <button type='button' onClick={ () => ResetActiveClient() } >Reset Active Client</button>
            <span style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
                <RadioCheckbox onChange={ () => ResetActiveClient() } />
                <p style={{paddingLeft: "0.4rem" }}>Disable/Enable</p>
            </span>
        </div>
    );
}
