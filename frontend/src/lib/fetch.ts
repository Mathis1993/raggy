import { getCsrfToken } from "$lib/cookies";

export async function fetchFromBackend(
  input: RequestInfo,
  init?: RequestInit,
): Promise<Response> {
  init = init || {};
  // Always include credentials
  init.credentials = "include";
  if (init && init.method && init.method.toUpperCase() !== "GET") {
    // Set X-CSRFToken header
    init.headers =
      init.headers instanceof Headers
        ? init.headers
        : new Headers(init.headers);
    (init.headers as Headers).append("X-CSRFToken", getCsrfToken());
    // Append CSRF token to body if it's a URLSearchParams
    init.body = init.body || new URLSearchParams();
    if (init.body instanceof URLSearchParams) {
      init.body.append("csrfmiddlewaretoken", getCsrfToken());
    }
  }

  return fetch(input, init);
}
