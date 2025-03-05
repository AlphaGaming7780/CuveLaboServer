

export async function getWaterLevel() : Promise<Number[]> {

    var value : Number[] = []

    try {
        const response = await fetch('/GetWaterLevel');
        if (!response.ok) {
            throw new Error(`Bad server response : ${response.statusText}`);
        }
        const data = await response.json();
        console.log(data);
        value = data;
    } catch (error) {
        throw new Error("Something went wrong in getWaterLevel().")
    }

    return value
};
