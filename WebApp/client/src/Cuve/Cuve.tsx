import React, {useContext, useEffect, useMemo, useRef, useState} from "react";
import classNames from "classnames";
import "./Cuve.css"
import { WaveWithLevel } from "../Wave/Wave.tsx";
import { WaterLevelContext } from "../API.tsx";

function getWaterLevel(level : number) {
    var WaveHeight = 0
    var SeaHeight = 0

    if(level < 0.05) {
        WaveHeight = level * 2 * 100
        SeaHeight = 0;
    } else if (level > 0.95) {
        WaveHeight = (1 - level) * 2 * 100
        SeaHeight = 100
    } else {
        WaveHeight = 10
        SeaHeight = level * 100 - 5
    }

    return { WaveHeight, SeaHeight }
}

interface CyclindreProps {WaterLevel : number};


const Cylindre = ( {WaterLevel} : CyclindreProps  ) : React.JSX.Element => {
    const relativeRef = useRef<HTMLDivElement>(null);
    const graduationRef = useRef<HTMLDivElement>(null);
    const [absolutePosition, setAbsolutePosition] = useState({ top: 0, left: 0 });
    const [ graduationVisible, setVisible ] = useState(false);
  
    useEffect(() => {
      const calculateAbsolutePosition = () => {
        if (relativeRef.current && graduationRef.current) {
          const rect = relativeRef.current.getBoundingClientRect();
          var cps = getComputedStyle(relativeRef.current)
          console.log(cps.borderTopWidth);
          setAbsolutePosition({
            top: rect.top + (1 - WaterLevel) * ( relativeRef.current.clientHeight ) + parseInt(cps.borderTopWidth) - graduationRef.current.clientHeight / 2 + window.scrollY,
            left: rect.left + window.scrollX + 0.75 * rect.width,
          });
          if(!graduationVisible) setVisible(true);
        }
      };
  
      calculateAbsolutePosition();
      window.addEventListener('resize', calculateAbsolutePosition);
      window.addEventListener('scroll', calculateAbsolutePosition);
  
      return () => {
        window.removeEventListener('resize', calculateAbsolutePosition);
        window.removeEventListener('scroll', calculateAbsolutePosition);
      };
    }, [WaterLevel, graduationVisible]);


    return (
        <div ref={relativeRef} className="cylindre" >
            <WaveWithLevel waterLevel={WaterLevel} />

            <div ref={graduationRef} className={classNames("graduation", graduationVisible ? "visible" : "")} style={{top:`${absolutePosition.top}px`, left:`${absolutePosition.left}px`}} >
                <div className="pointer" />
                <div className="panel">
                    <p>{(WaterLevel*100).toFixed(1)}%</p>
                </div>
            </div> 
        </div>
    )
}

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

    // var p0 : CyclindreProps = { WaterLevel:WaterLevel[0], WaveHeight:WaterLevel0.WaveHeight, SeaHeight:WaterLevel0.SeaHeight}
    // const Cylindre0Memo = useMemo( () => Cylindre(p0) , [p0] )

    const CylindreContainerMemo = useMemo( () => CylindreContainer(WaterLevel), [WaterLevel] )


    return (
        <div className="cuve">

            {CylindreContainerMemo}

            <div className="tank">
                <WaveWithLevel waterLevel={0.5} />
            </div>

        </div>
    )
}
