
export interface SetMotorsSpeedProps {
    MotorIndex : number,
    MotorSpeed : number,
}

export const SetMotorsSpeed = ( {MotorIndex = -1, MotorSpeed = -1 } : SetMotorsSpeedProps) => {

    var data = {
        "MotorIndex": MotorIndex,
        "MotorSpeed": MotorSpeed
    }

    fetch('/SetMotorsSpeed', {

        cache: "no-cache",
        method: 'POST', 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
  
    })
}