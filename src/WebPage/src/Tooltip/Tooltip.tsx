import React from "react";
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
    return (
        <div className={classNames("tooltip-container", alwaysDisplay ? "forceShow" : "")}>
            <span className={classNames("tooltip", direction)}>{content}</span>
            <span className="tooltip-child" >{children}</span>
        </div>
    )
}