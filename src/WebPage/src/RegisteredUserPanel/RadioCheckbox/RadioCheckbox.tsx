import React, { JSX, useEffect, useState } from 'react';
import './RadioCheckbox.css';

export interface RadioCheckboxProps {
    checked?: boolean;
    onChange?: (checked: boolean) => void;
}

export const RadioCheckbox = ({ checked = false, onChange } : RadioCheckboxProps ) : JSX.Element => {

    const [isChecked, setIsChecked] = useState(false);

    const handleCheckboxChange = () => {
        // onChange && onChange(!checked);
        setIsChecked(!isChecked);
        onChange && onChange(!isChecked);
    };

    // useEffect(() => {

    //     if (isChecked !== checked) setIsChecked(checked);

    // }, [checked]);

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