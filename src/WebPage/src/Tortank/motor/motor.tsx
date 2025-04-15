import React, { useEffect, useState } from "react";
import "./Motor.css"
import { Tooltip, TooltipDirection } from "../../Tooltip/Tooltip.tsx";

export interface MotorProps {
    MotorSpeed : number
    OnMotorSpeedChange: (value: number) => void
}

export const Motor = (  {MotorSpeed, OnMotorSpeedChange}  : MotorProps) : any => {

    if(MotorSpeed < 0) MotorSpeed = 0;
    const [motorSpeed, SetMotorSpeed] = useState(MotorSpeed)

    useEffect(() => {
        SetMotorSpeed(MotorSpeed)
    }, [MotorSpeed])

    const MotorTooltip = () => {
        return (
            <div className="MotorTooltip">
                <input id="MotorSpeedRangeInput" title="MotorSpeedRangeInput" name="MotorSpeedRangeInput" type="range" step={0.01} value={motorSpeed} max={1} min={0} onChange={ (value) => SetMotorSpeed(parseFloat(value.target.value)) } onMouseUp={ () => { if(MotorSpeed !== motorSpeed) OnMotorSpeedChange(motorSpeed) } } ></input>
                <label form="MotorSpeedRangeInput" style={{marginLeft:"0.5rem", marginBottom:"0"}} >{`${(motorSpeed*100).toFixed(1)}%`}</label>
            </div>
        )
    }

    return (
        <Tooltip content={MotorTooltip()} direction={TooltipDirection.Left} alwaysDisplay={true}>
            <div className="Motor" >
                <div className="inner" >

                </div>
                
            </div>
        </Tooltip>

    )
}