import {getDocuments} from "./documentService";
import {page} from "$app/stores";

// Only run client-side to ensure credentials are available for fetch function
export const ssr = false;

/** @type {import('./$types').PageLoad} */
export async function load({ params, url }) {
    const documentType = url.searchParams.get('type') || "";
    const search = url.searchParams.get('search') || "";
    const documents = await getDocuments(documentType, search);
    documents.currentPage = 1;
    return documents;
}
