import {getCsrfToken} from "$lib/cookies";

export async function signUp(formData: { email: string; password1: string; password2: string, first_name: string; last_name: string}) {
    const response = await fetch('http://127.0.0.1:8000/users/signup/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(formData),
    });

    if (response.status !== 201) {
        const error = await response.json();
        throw error;
    }
    return response.json();
}


export async function login(email: string, password: string) {
    const body = new URLSearchParams({
        'email': email,
        'password': password,
        'csrfmiddlewaretoken': getCsrfToken(),
    });

    const response = await fetch('http://127.0.0.1:8000/users/login/', {
        method: 'POST',
        credentials: 'include',
        body: body,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    if (response.status !== 200) {
        const error = await response.json();
        throw error;
    }
    return response.json();
}