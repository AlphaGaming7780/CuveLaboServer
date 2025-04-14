import React, { JSX, useState } from 'react';
import './RadioCheckbox.css';

export const RadioCheckbox = () : JSX.Element => {

    const [isChecked, setIsChecked] = useState(false);

    const handleCheckboxChange = () => {
        setIsChecked(!isChecked);
    };

    return (
        <>
            <div>
                <input type="checkbox" id="checkboxInput" checked={isChecked} onChange={handleCheckboxChange}/>
                <label htmlFor="checkboxInput" className="toggleSwitch">
                </label>
            </div>
        </>
    )
}