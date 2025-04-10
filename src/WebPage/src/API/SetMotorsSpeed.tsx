
export interface SetMotorsSpeedProps {
    MotorIndex : number,
    MotorSpeed : number,
}

export const SetMotorSpeed = ( {MotorIndex = -1, MotorSpeed = -1 } : SetMotorsSpeedProps) => {

    var data = {
        "MotorIndex": MotorIndex,
        "MotorSpeed": MotorSpeed
    }

    fetch('/SetMotorSpeed', {

        cache: "no-cache",
        method: 'POST', 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
  
    })
}