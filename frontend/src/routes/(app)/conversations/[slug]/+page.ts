

export async function load({ params }: { params: any }) {
    console.log("Making request to http://127.0.0.1:8000/api/conversations");
    let conversationId: number = params.slug
    const response = await fetch('http://127.0.0.1:8000/api/conversations/' + conversationId + '/', { credentials: 'include' });
    const conversation = await response.json();
    console.log(conversation)
    return {"conversation": conversation}
}