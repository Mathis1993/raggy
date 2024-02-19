export const ssr = false;

/** @type {import('../../../../../../.svelte-kit/types/src/routes').PageLoad} */
export async function load({ params}) {
		const uidb64 = params.uidb64;
		const token = params.token;
		return {
			uidb64: uidb64,
			token: token
		}
}