import {invalidateAll} from "$app/navigation";
import { getCsrfToken } from '$lib/cookies';

const DOCUMENT_API_ENDPOINT: string = 'http://127.0.0.1:8000/api/documents/';


export async function getDocuments() {
    const response = await fetch(DOCUMENT_API_ENDPOINT, {credentials: 'include'});
    if (!response.ok) {
        console.error('Failed to fetch documents', response.status);
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
        console.error('Failed to delete document', response.status);
    }
}


export async function createDocument(document_url: string) {
    const response = await fetch(DOCUMENT_API_ENDPOINT, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({'document_url': document_url})
    });

    if (response.ok) {
        let createdDocument: ContextDocument = await response.json();
        return createdDocument;
    } else {
        console.error('Error in API response');
        return null;
    }
}