export async function load({ params, fetch }) {
    let conversationId = params.slug;
    try {
        const response = await fetch(`http://localhost:8000/api/conversations/${conversationId}/`);

        if (!response.ok) {
            console.error('Failed to fetch conversation:', response.status);
            return { status: response.status, error: new Error('Conversation not found') };
        }

        const conversation = await response.json();
        return { conversation };
    } catch (error) {
        console.error('Error fetching conversation:', error);
        return { status: 500, error };
    }
}
