import React, { useEffect, useRef, useState } from "react";
import "./Tooltip.css"
import classNames from "classnames";

export enum TooltipDirection {
    Top = "Top",
    Bottom = "Bottom",
    Left = "Left",
    Right = "Right"
}

export interface TooltipProps {
    alwaysDisplay?: boolean
    direction?: TooltipDirection
    content: any
    children: any
}

export const Tooltip = ( {children, content, direction = TooltipDirection.Top, alwaysDisplay=false , ...a} : TooltipProps ) => {

    const refParent = useRef<HTMLDivElement>(null)
    const refTooltip = useRef<HTMLSpanElement>(null)
    const refTooltipMarker = useRef<HTMLDivElement>(null)

    const [ tooltipPos, SetTooltipPos ] = useState<number[]>( [0, 0] )
    const [ tooltipMarkerPos, SetTooltipMarkerPos ] = useState<number[]>( [0, 0] )
    const [ canBeVisible, SetCanBeVidsible ] = useState(false)

    useEffect( () => {

        if(refParent.current == null || refTooltip.current == null || refTooltipMarker.current == null) return;

        var tooltipPosTop = 0
        var tooltipPosLeft = 0

        if(direction === TooltipDirection.Left) {
            tooltipPosTop = refParent.current.clientTop + refParent.current.clientHeight / 2 - refTooltip.current.clientHeight / 2
            tooltipPosLeft = refParent.current.clientLeft - refTooltip.current.clientWidth - refTooltipMarker.current.clientWidth / 2;
        } else if ( direction === TooltipDirection.Top ) {
            tooltipPosTop = refParent.current.clientTop + refTooltip.current.clientHeight;
            tooltipPosLeft = refParent.current.clientLeft + refParent.current.clientWidth / 2 - refTooltip.current.clientWidth / 2;
        }

        var tooltipMarkerTopPos = 0
        var tooltipLeftPos = 0

        if(direction === TooltipDirection.Left) {
            tooltipMarkerTopPos = tooltipPosTop + refTooltip.current.clientHeight / 2 - refTooltipMarker.current.clientHeight / 2
            tooltipLeftPos = tooltipPosLeft + refTooltip.current.clientWidth //+ refTooltipMarker.current.clientWidth / 2;
        }

        SetTooltipPos([tooltipPosTop, tooltipPosLeft])
        SetTooltipMarkerPos([tooltipMarkerTopPos, tooltipLeftPos])
        SetCanBeVidsible(true)

    }, [refParent, refTooltip, refTooltipMarker, direction])

    return (
        <div ref={refParent} className={classNames("tooltip-container", alwaysDisplay && canBeVisible ? "forceShow" : "")}>
            <span ref={refTooltip} className={classNames("tooltip")} style={{top:tooltipPos[0], left:tooltipPos[1]}} >{content}</span>
            <span ref={refTooltipMarker} className={classNames("Tooltip-panel-marker", direction)} style={{top:tooltipMarkerPos[0], left:tooltipMarkerPos[1]}} ></span>
            <span className="tooltip-child" >{children}</span>
        </div>
    )
}