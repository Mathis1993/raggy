

export async function load({ params }: { params: any }) {
    console.log("Making request to http://localhost:8000/api/documents");
    let documentId: number = params.slug
    const response = await fetch('http://localhost:8000/api/documents/' + documentId + '/');
    const document = await response.json();
    console.log(document)
    return document;
}