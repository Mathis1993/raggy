/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {
    const response = await fetch('http://localhost:8000/api/questions/');
    return await response.json();
}