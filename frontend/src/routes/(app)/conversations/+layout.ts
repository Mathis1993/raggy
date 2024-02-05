/** @type {import('../../../../.svelte-kit/types/src/routes').PageLoad} */
export async function load({ params }: { params: any }) {
    const response = await fetch('http://127.0.0.1:8000/api/conversations/', { credentials: 'include' });
    let data = await response.json()
    return {"conversations": data}
}