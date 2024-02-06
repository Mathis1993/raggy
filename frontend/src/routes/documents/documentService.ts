const DOCUMENT_API_ENDPOINT: string = 'http://localhost:8000/api/documents/';


export async function getDocuments() {
    const response = await fetch(DOCUMENT_API_ENDPOINT);
    if (!response.ok) {
        console.error('Failed to fetch documents', response.status);
        return [];
    }
    return await response.json();
}

export async function retrieveDocument(documentId: number) {
    const response = await fetch('http://localhost:8000/api/documents/' + documentId + '/');
    const document: ContextDocument = await response.json();
    return document;
}


export async function deleteDocument(documentId: number) {
    const response = await fetch('http://localhost:8000/api/documents/' + documentId + '/', {
        method: 'DELETE',
    });
    if (!response.ok) {
        console.error('Failed to delete document', response.status);
    }
}


export async function createDocument(document_url: string) {
    const response = await fetch(DOCUMENT_API_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'document_url': document_url})
    });

    if (response.ok) {
        let apiResponse = await response.json();
        console.log(apiResponse);
    } else {
        console.error('Error in API response');
    }
}