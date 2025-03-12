import React, {useContext, useMemo} from "react";
import "./Cuve.css"
import { WaveWithLevel } from "../../Wave/Wave.tsx";
import { Cylindre } from "../Cylindre/Cylindre.tsx";
import { UpdatedValueContext } from "../../API/UpdatedValue.tsx";
import { Motor } from "../motor/motor.tsx";
import { Tooltip, TooltipDirection } from "../../Tooltip/Tooltip.tsx";

const CylindreContainer = (WaterLevel : number[]) => {
    return (
        <div className="cylindre-container" >
            <Cylindre WaterLevel={WaterLevel[0]} />
            <Cylindre WaterLevel={WaterLevel[1]} />
            <Cylindre WaterLevel={WaterLevel[2]} />
        </div>
    )
}

export function Cuve() : React.JSX.Element {

    const { WaterLevel, MotorSpeed } = useContext(UpdatedValueContext)
    const CylindreContainerMemo = useMemo( () => CylindreContainer(WaterLevel), [WaterLevel] )

    return (
        <div className="cuve">

            <div className="top">
                <div>
                    <Tooltip content={`${(MotorSpeed[0]*100).toFixed(1)}%`} direction={TooltipDirection.Left} alwaysDisplay={true}><Motor/></Tooltip>
                    <Tooltip content={`${(MotorSpeed[1]*100).toFixed(1)}%`} direction={TooltipDirection.Left} alwaysDisplay={true} ><Motor/></Tooltip>
                </div>

                {CylindreContainerMemo}

            </div>

            

            <div className="tank">
                <WaveWithLevel waterLevel={0.5} waveMaxHeight={0.5} />
            </div>

        </div>
    )
}
