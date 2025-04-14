import React, { JSX } from 'react';
import './RadioCheckbox.css';

export const RadioCheckbox = () : JSX.Element => {

    return (
        <>
            <input type="checkbox" id="checkboxInput"></input>
            <label form="checkboxInput" className="toggleSwitch"></label>
        </>
    )
}