import {invalidateAll} from "$app/navigation";

const DOCUMENT_API_ENDPOINT = "http://localhost:8000/api/documents/";


export async function getDocuments() {
    const response = await fetch(DOCUMENT_API_ENDPOINT);
    if (!response.ok) {
        console.error("Failed to fetch documents", response.status);
        return [];
    }
    return await response.json();
}

export async function retrieveDocument(documentId: number) {
    const response = await fetch("http://localhost:8000/api/documents/" + documentId + "/");
    const document: ContextDocument = await response.json();
    return document;
}


export async function deleteDocument(documentId: number) {
    const response = await fetch("http://localhost:8000/api/documents/" + documentId + "/", {
        method: "DELETE",
    });
    if (!response.ok) {
        console.error("Failed to delete document", response.status);
    }
}


export async function createDocumentFromUrl(document_url: string) {
    const response = await fetch(`${DOCUMENT_API_ENDPOINT}create_from_url/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
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
        method: "POST",
        body: formData,  // browser automatically sets the correct headers
    });

    if (response.ok) {
        return await response.json();
    } else {
        const errorResponse = await response.json(); // Assuming error response structure { error: "ErrorMessage" }
        throw new Error(errorResponse.error || 'An unknown error occurred');
    }
}
