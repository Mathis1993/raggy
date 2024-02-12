import {getDocuments} from "./documentService";

// Only run client-side to ensure credentials are available for fetch function
export const ssr = false;

/** @type {import('./$types').PageLoad} */
export async function load({ params, url }) {
    const documentType = url.searchParams.get('type') || "all";
    console.log("documentType", documentType);
    const documents = await getDocuments(documentType);
    return {documents: documents};
}
