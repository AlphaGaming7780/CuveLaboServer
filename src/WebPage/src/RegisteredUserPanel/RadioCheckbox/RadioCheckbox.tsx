import React, { JSX, useState } from 'react';
import './RadioCheckbox.css';

export interface RadioCheckboxProps {
    onChange?: (checked: boolean) => void;
}

export const RadioCheckbox = ({ onChange } : RadioCheckboxProps ) : JSX.Element => {

    const [isChecked, setIsChecked] = useState(false);

    const handleCheckboxChange = () => {
        onChange && onChange(!isChecked);
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