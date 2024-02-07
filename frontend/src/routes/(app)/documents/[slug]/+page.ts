

export async function load({ fetch, params }) {
    console.log("Making request to http://127.0.0.1:8000/api/documents");
    const documentId: string = params.slug
    const response = await fetch('http://127.0.0.1:8000/api/documents/' + documentId + '/', { credentials: 'include' });
    const document = await response.json();
    console.log(document)
    return document;
}