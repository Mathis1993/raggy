import { type Writable, writable } from 'svelte/store';

export const visible: Writable<boolean> = writable(false);