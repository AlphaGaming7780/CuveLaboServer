
export const PostData = async <T = any>(url : string, data : T) => {
    const response = await fetch(url, {
        cache: "no-cache",
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        throw new Error(`Bad server response : ${response.statusText}`);
    }
}