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
            <RadioCheckbox />
        </div>
    );
}
