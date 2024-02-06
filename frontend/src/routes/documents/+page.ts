import {getDocuments} from "./documentService";

/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {
    return await getDocuments();
}