import { type Writable, writable } from 'svelte/store';

export const user: Writable<User> = writable({} as User);