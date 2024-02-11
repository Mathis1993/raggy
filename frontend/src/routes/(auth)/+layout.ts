// Run the load function always client-side
export const ssr = false;

/** @type {import('../../../../.svelte-kit/types/src/routes').PageLoad} */
// Get the csrf token and set it as a cookie on the client in preparation of the login POST request
// (httpOnly is false as we need to extract the token from the cookie for later client-side post requests)
// (but django docs say that is okay -> https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-CSRF_COOKIE_HTTPONLY)
export async function load({ fetch }) {
	const response = await fetch('http://127.0.0.1:8000/users/csrf/', {credentials: 'include'});
	return await response.json();
}