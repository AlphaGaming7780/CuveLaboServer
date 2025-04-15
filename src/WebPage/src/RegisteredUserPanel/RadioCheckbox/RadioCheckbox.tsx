import React, { JSX, useState } from 'react';
import './RadioCheckbox.css';

export interface RadioCheckboxProps {
    checked?: boolean;
    onChange?: (checked: boolean) => void;
}

export const RadioCheckbox = ({ checked = false, onChange } : RadioCheckboxProps ) : JSX.Element => {

    // const [isChecked, setIsChecked] = useState(false);

    const handleCheckboxChange = () => {
        onChange && onChange(!checked);
        // onChange && onChange(!isChecked);
        // setIsChecked(!isChecked);
    };

    return (
        <>
            <div>
                <input type="checkbox" id="checkboxInput" checked={checked} onChange={handleCheckboxChange}/>
                <label htmlFor="checkboxInput" className="toggleSwitch">
                </label>
            </div>
        </>
    )
}