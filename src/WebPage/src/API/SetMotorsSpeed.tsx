

export const SetMotorsSpeed = (Motor1Speed : number = -1, Motor2Speed: number = -1) => {

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