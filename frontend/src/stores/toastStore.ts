import {type Writable, writable} from "svelte/store";

export const toasts: Writable<Toast[]> = writable([]);


export const addToast = (message: string, type: string) => {
    const id: number = Math.floor(Math.random() * 10000);

    const defaults = {
        id,
        dismissable: true,
    };
    let toast: Toast = {message: message, type: type, ...defaults};
    toasts.update((all) => [toast, ...all]);

};

export const dismissToast = (id) => {
    toasts.update((all) => all.filter((t) => t.id !== id));
};
