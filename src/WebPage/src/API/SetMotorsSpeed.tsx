
export interface SetMotorsSpeedProps {
    Motor1Speed?: number, 
    Motor2Speed?: number
}

export const SetMotorsSpeed = ( {Motor1Speed = -1, Motor2Speed = -1 } : SetMotorsSpeedProps) => {

    var data = {
        "Motor1Speed": Motor1Speed,
        "Motor2Speed": Motor2Speed
    }

    fetch('/SetMotorsSpeed', {

        cache: "no-cache",
        method: 'POST', 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
  
    })
}