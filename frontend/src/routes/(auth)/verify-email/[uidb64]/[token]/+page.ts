import { verifyEmail } from '../../../authService';

export const ssr = false;

/** @type {import('../../../../../../.svelte-kit/types/src/routes').PageLoad} */
export async function load({ params}) {
	try {
		const uidb64 = params.uidb64;
		const token = params.token;
		return await verifyEmail(uidb64, token);
	} catch (error) {
		return { status: 500, error };
	}
}