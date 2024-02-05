/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {
    const response = await fetch('http://127.0.0.1:8000/api/documents/', { credentials: 'include' });
    return await response.json();
}