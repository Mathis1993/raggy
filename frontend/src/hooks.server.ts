import { redirect } from '@sveltejs/kit';
import { createEventDispatcher } from 'svelte';

const unProtectedRoutes = ['/login', '/signup', '/logout'];
export const handle = async ({ event, resolve }) => {
	console.log("hook");
	console.log(event.url.pathname);
	const sessionId = event.cookies.get('sessionid');
	const isAuthenticated = sessionId !== undefined;
	// ToDo: Check expiration date of the sessionid cookie
	if (!isAuthenticated && !unProtectedRoutes.includes(event.url.pathname)) {
		return redirect(303, '/login');
	}

	// ToDo: Delete cookies if logout request
	// ToDo: Delete session from server in logout action
	if (event.url.pathname === '/logout') {
		event.cookies.delete('sessionid', { path: '/'});
		event.cookies.delete('csrftoken', { path: '/'});
		return redirect(303, '/login');
	}

	return resolve(event);
}