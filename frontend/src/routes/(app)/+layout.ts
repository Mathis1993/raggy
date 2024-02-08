/** @type {import('../../../.svelte-kit/types/src/routes').PageLoad} */
export async function load({ fetch }) {
    const response = await fetch('http://127.0.0.1:8000/api/conversations/', {credentials: 'include'});
    const data = await response.json()
    console.log("Loaded conversations")
    return {"conversations": data}
}