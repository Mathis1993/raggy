import { getCsrfToken } from "$lib/cookies";
import { fetchFromBackend } from "$lib/fetch";

export const DOCUMENT_API_ENDPOINT: string =
  "http://127.0.0.1:8000/api/documents/";

export async function getDocuments(
  documentType: string = "",
  search: string = "",
  page: number = 1,
) {
  let queryParams = new URLSearchParams();
  if (documentType && documentType !== "all") {
    queryParams.append("type", documentType);
  }
  if (search) {
    queryParams.append("search", search);
  }
  queryParams.append("page", page.toString());
  const response = await fetchFromBackend(
    DOCUMENT_API_ENDPOINT + "?" + queryParams.toString(),
  );
  if (!response.ok) {
    console.error("Failed to fetch documents", response.status);
    return [];
  }
  let documentResponse = await response.json();
  documentResponse.page = page;
  return documentResponse;
}

export async function retrieveDocument(documentId: number) {
  const response = await fetchFromBackend(
    "http://127.0.0.1:8000/api/documents/" + documentId + "/",
  );
  const document: ContextDocument = await response.json();
  return document;
}

export async function deleteDocument(documentId: number) {
  const response = await fetchFromBackend(
    "http://127.0.0.1:8000/api/documents/" + documentId + "/",
    {
      method: "DELETE",
    },
  );
  if (!response.ok) {
    console.error("Failed to delete document", response.status);
  }
}

export async function createDocumentFromUrl(document_url: string) {
  const response = await fetchFromBackend(
    `${DOCUMENT_API_ENDPOINT}create_from_url/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ document_url: document_url }),
    },
  );

  if (response.ok) {
    return await response.json(); // Assuming this returns the created document
  } else {
    const errorResponse = await response.json(); // Assuming error response structure { error: "ErrorMessage" }
    throw new Error(errorResponse.error || "An unknown error occurred");
  }
}

export async function createDocumentFromFileUpload(
  file: File,
  documentName: string,
) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("document_name", documentName ? documentName : file.name);

  const response = await fetchFromBackend(`${DOCUMENT_API_ENDPOINT}upload/`, {
    method: "POST",
    body: formData, // browser automatically sets the correct headers
  });

  if (response.ok) {
    return await response.json();
  } else {
    const errorResponse = await response.json(); // Assuming error response structure { error: "ErrorMessage" }
    throw new Error(errorResponse.error || "An unknown error occurred");
  }
}
