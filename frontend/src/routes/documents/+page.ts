/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {
    const response = await fetch('http://localhost:8000/api/documents/');
    return await response.json();
}