import { parse } from 'cookie';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ cookies }) {
	const response = await fetch('http://127.0.0.1:8000/users/csrf/', {credentials: 'include'});
	const setCookieHeader = response.headers.get('set-cookie');

	if (setCookieHeader) {
		const parsedCookies = parse(setCookieHeader);
		const csrfToken = parsedCookies['csrftoken'];

		if (csrfToken) {
			cookies.set('csrftoken', csrfToken,  { path: '/'});
		}
	}
	return await response.json();
}

export const actions = {
	post: async ({ cookies, request }) => {
		const data = await request.formData();
		const email = data.get('email') as string;
		const password = data.get('password') as string;

		const csrfToken = cookies.get('csrftoken') as string;
		console.log('csrfToken', csrfToken);

		const headers: Record<string, string> = {
			'Content-Type': 'application/x-www-form-urlencoded',
		};

		if (csrfToken) {
			headers['Cookie'] = `csrftoken=${csrfToken}`;
		}

		// const body = JSON.stringify({ email: email, password: password, csrfmiddlewaretoken: csrfToken });
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