export const GetData = async <T = any>(url : string) : Promise<T> => {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Bad server response : ${response.statusText}`);
        // return null;
    }
    const data = await response.json();
    return data;
}