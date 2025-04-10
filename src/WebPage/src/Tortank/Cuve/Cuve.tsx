import React, {JSX, useContext, useMemo} from "react";
import "./Cuve.css"
import { WaveWithLevel } from "../../Wave/Wave.tsx";
import { Cylindre } from "../Cylindre/Cylindre.tsx";
import { UpdatedValueContext } from "../../API/UpdatedValue.tsx";
import { Motor } from "../motor/motor.tsx";
import { SetMotorSpeed } from "../../API/SetMotorsSpeed.tsx";
import { BaseDataContext } from "../../API/GetBaseData.tsx";

const CylindreContainer = ( numberOfCuve : number, WaterLevel : number[]) => {
        
    return (
        <div className="cylindre-container" >
            {WaterLevel.map( (waterLevel) => { 
                return <Cylindre WaterLevel={waterLevel} />
            } )}
            {/* <Cylindre WaterLevel={WaterLevel[0]} />
            <Cylindre WaterLevel={WaterLevel[1]} />
            <Cylindre WaterLevel={WaterLevel[2]} /> */}
        </div>
    )
}

export function Cuve() : React.JSX.Element {
    const { numberOfCuve, numberOfMotor } = useContext(BaseDataContext)
    const { WaterLevel, MotorSpeed } = useContext(UpdatedValueContext)
    const CylindreContainerMemo = useMemo( () => CylindreContainer(numberOfCuve, WaterLevel), [WaterLevel, numberOfCuve] )

    let data : Array<JSX.Element> = []

    if(MotorSpeed.length !== numberOfMotor) return <></>
    if(WaterLevel.length !== numberOfCuve ) return <></>

    for (let i = 0; i < numberOfMotor; i++) {
        data[i] = <Motor MotorSpeed={MotorSpeed[i]} OnMotorSpeedChange={(value) => SetMotorSpeed({ MotorIndex:i, MotorSpeed:value })}/>
    }

    return (
        <div className="cuve">

            <div className="top">
                <div>
                    {data}
                    {/* <Motor MotorSpeed={MotorSpeed[0]} OnMotorSpeedChange={(value) => SetMotorsSpeed({Motor1Speed:value})}/> */}
                    {/* <Motor MotorSpeed={MotorSpeed[1]} OnMotorSpeedChange={(value) => SetMotorsSpeed({Motor2Speed:value})} /> */}
                </div>

                {CylindreContainerMemo}

            </div>

            <div className="tank">
                <WaveWithLevel waterLevel={0.5} waveMaxHeight={0.5} />
            </div>

        </div>
    )
}
