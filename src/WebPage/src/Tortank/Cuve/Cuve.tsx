import React, {useContext, useMemo} from "react";
import "./Cuve.css"
import { WaveWithLevel } from "../../Wave/Wave.tsx";
import { WaterLevelContext } from "../../API.tsx";
import { Cylindre } from "../Cylindre/Cylindre.tsx";


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

    const WaterLevel = useContext(WaterLevelContext)
    const CylindreContainerMemo = useMemo( () => CylindreContainer(WaterLevel), [WaterLevel] )

    return (
        <div className="cuve">

            {CylindreContainerMemo}

            <div className="tank">
                <WaveWithLevel waterLevel={0.5} waveMaxHeight={0.5} />
            </div>

        </div>
    )
}
