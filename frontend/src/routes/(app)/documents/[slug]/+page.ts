

export async function load({ params }: { params: any }) {
    console.log("Making request to http://127.0.0.1:8000/api/documents");
    let documentId: number = params.slug
    const response = await fetch('http://127.0.0.1:8000/api/documents/' + documentId + '/', { credentials: 'include' });
    const document = await response.json();
    console.log(document)
    return document;
}