type User = {
	email: string;
	first_name: string | null;
	last_name: string | null;
	settings: {
		language: string;
	};
}