import { getCsrfToken } from '$lib/cookies';

const DOCUMENT_API_ENDPOINT: string = 'http://127.0.0.1:8000/api/documents/';


export async function getDocuments(documentType: string = "all", search: string = "") {
    let queryParams = new URLSearchParams();
    queryParams.append('type', documentType);
    queryParams.append('search', search);
    const response = await fetch(DOCUMENT_API_ENDPOINT + "?" + queryParams.toString(), {credentials: 'include'});
    if (!response.ok) {
        console.error("Failed to fetch documents", response.status);
        return [];
    }
    return await response.json();
}

export async function retrieveDocument(documentId: number) {
    const response = await fetch('http://127.0.0.1:8000/api/documents/' + documentId + '/', {credentials: 'include'});
    const document: ContextDocument = await response.json();
    return document;
}


export async function deleteDocument(documentId: number) {
    const response = await fetch('http://127.0.0.1:8000/api/documents/' + documentId + '/', {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        }
    });
    if (!response.ok) {
        console.error("Failed to delete document", response.status);
    }
}


export async function createDocumentFromUrl(document_url: string) {
    const response = await fetch(`${DOCUMENT_API_ENDPOINT}create_from_url/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({"document_url": document_url})
    });

    if (response.ok) {
        return await response.json(); // Assuming this returns the created document
    } else {
        const errorResponse = await response.json(); // Assuming error response structure { error: "ErrorMessage" }
        throw new Error(errorResponse.error || 'An unknown error occurred');
    }
}

export async function createDocumentFromFileUpload(file: File, documentName: string) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("document_name", documentName ? documentName : file.name);

    const response = await fetch(`${DOCUMENT_API_ENDPOINT}upload/`, {
        method: 'POST',
        credentials: 'include',
        body: formData,  // browser automatically sets the correct headers
        headers: {
            'X-CSRFToken': getCsrfToken(),
        }
    });

    if (response.ok) {
        return await response.json();
    } else {
        const errorResponse = await response.json(); // Assuming error response structure { error: "ErrorMessage" }
        throw new Error(errorResponse.error || 'An unknown error occurred');
    }
}
