import { parse } from 'cookie';
import { redirect } from '@sveltejs/kit';

/** @type {import('../../../../.svelte-kit/types/src/routes').PageLoad} */
// Get the csrf token and set it as a cookie on the client in preparation of the login POST request
// (httpOnly is false as we need to extract the token from the cookie for later client-side post requests)
// (but django docs say that is okay -> https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-CSRF_COOKIE_HTTPONLY)
export async function load({ cookies }) {
	const response = await fetch('http://127.0.0.1:8000/users/csrf/', {credentials: 'include'});
	const setCookieHeader = response.headers.get('set-cookie');

	if (setCookieHeader) {
		const parsedCookies = parse(setCookieHeader);
		const csrfToken = parsedCookies['csrftoken'];

		if (csrfToken) {
			cookies.set('csrftoken', csrfToken,  { path: '/', httpOnly: false});
		}
	}
	return await response.json();
}

export const actions = {
	// Log in setting the sessionid cookie
	post: async ({ cookies, request }) => {
		const data = await request.formData();
		const email = data.get('email') as string;
		const password = data.get('password') as string;

		const csrfToken = cookies.get('csrftoken') as string;
		const sessionId = cookies.get('sessionid') as string;

		const headers: Record<string, string> = {
			'Content-Type': 'application/x-www-form-urlencoded',
		};

		if (csrfToken) {
			headers['Cookie'] = `csrftoken=${csrfToken}`;
		}
		if (csrfToken && sessionId) {
			headers['Cookie'] += `; sessionid=${sessionId}`;
		}

		const body = new URLSearchParams({
			email: email,
			password: password,
			csrfmiddlewaretoken: csrfToken,
		});

		const response = await fetch('http://127.0.0.1:8000/users/login/', {
			method: 'POST',
			credentials: 'include',
			headers: headers,
			body: body,
		});
		if (response.status != 200) {

			const error = await response.json();
			return { status: 'error', error };
		} else {
			const setCookieHeader = response.headers.get('set-cookie');
			if (setCookieHeader) {
				const cookiesSeparated = setCookieHeader.split(',').map(cookie => parse(cookie.trim()));
				const sessionIdCookie = cookiesSeparated.find(cookie => 'sessionid' in cookie);
				const sessionId = sessionIdCookie ? sessionIdCookie['sessionid'] : undefined;

				if (sessionId) {
					cookies.set('sessionid', sessionId,  { path: '/'});
				}
			}
			redirect(302, '/')
		}
	}
}