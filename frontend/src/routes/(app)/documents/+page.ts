import {getDocuments} from "./documentService";

// Only run client-side to ensure credentials are available for fetch function
export const ssr = false;

/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {
    const documents = await getDocuments();
    return {documents: documents};
}
