import React, {useEffect, useRef, useState} from "react";
import classNames from "classnames";
import "./Cylindre.css"
import { WaveWithLevel } from "../../Wave/Wave.tsx";

interface CyclindreProps {WaterLevel : number};

export const Cylindre = ( {WaterLevel} : CyclindreProps  ) : React.JSX.Element => {
    if(WaterLevel < 0) WaterLevel = 0
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