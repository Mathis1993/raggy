/** @type {import('../../../.svelte-kit/types/src/routes').PageLoad} */
export async function load({ fetch }) {
    const conversationsResponse = await fetch('http://127.0.0.1:8000/api/conversations/', {credentials: 'include'});
    const conversations = await conversationsResponse.json()
    console.log("Loaded conversations")
    const userResponse = await fetch('http://127.0.0.1:8000/users/info/', {credentials: 'include'});
    const user: User = await userResponse.json()
    console.log("Loaded user info")
    return {"conversations": conversations, "user": user, "conversationsLoaded": true}
}