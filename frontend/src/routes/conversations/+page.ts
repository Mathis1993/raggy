/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {
    const response = await fetch('http://localhost:8000/api/conversations/');
    let data = await response.json()
    return {"conversations": data}
}