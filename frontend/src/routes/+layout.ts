/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
    const response = await fetch('http://localhost:8000/api/conversations/');
    let data = await response.json()
    console.log("Loaded conversations")
    return {"conversations": data}
}