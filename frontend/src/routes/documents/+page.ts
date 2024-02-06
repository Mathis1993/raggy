import {getDocuments} from "./documentService";

/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {
    let documents = await getDocuments();
    return {documents: documents};
}
