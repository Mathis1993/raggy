import {getCsrfToken} from "$lib/cookies";
import { visible, visibleText } from '../../stores/visibleStore';

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
    visible.set(true);
    visibleText.set('You need to verify your email address before you can sign in. Please check your email for a verification link.\nDon\'t forget to check your spam folder!')
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

export async function requestPasswordReset(email: string) {
    const body = new URLSearchParams({
        'email': email,
        'csrfmiddlewaretoken': getCsrfToken(),
    });

    const response = await fetch('http://127.0.0.1:8000/users/request-password-reset/', {
        method: 'POST',
        credentials: 'include',
        body: body,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    if (response.status !== 200) {
        throw await response.json();
    }

    return response.json();
}

export async function verifyEmail(uidb64: string, token: string) {
    const body = new URLSearchParams({
        'csrfmiddlewaretoken': getCsrfToken(),
        'uidb64': uidb64,
        'token': token,
    }
    );
    const response = await fetch('http://127.0.0.1:8000/users/verify-email/', {
        method: 'POST',
        credentials: 'include',
        body: body,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    if (response.status !== 200) {
        throw await response.json();
    }

    return response.json();
}

export async function resetPassword(uidb64: string, token: string, password1: string, password2: string) {
    const body = new URLSearchParams({
          'csrfmiddlewaretoken': getCsrfToken(),
          'uidb64': uidb64,
          'token': token,
          'password1': password1,
          'password2': password2,
      }
    );
    const response = await fetch('http://127.0.0.1:8000/users/reset-password/', {
        method: 'POST',
        credentials: 'include',
        body: body,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    if (response.status !== 200) {
        throw await response.json();
    }
    visible.set(true);
    visibleText.set('Your password has been reset. You can now sign in with your new password.')
    return response.json();
}