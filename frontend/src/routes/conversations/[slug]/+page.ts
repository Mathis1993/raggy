

export async function load({ params }: { params: any }) {
    console.log("Making request to http://localhost:8000/api/conversations");
    let conversationId: number = params.slug
    const response = await fetch('http://localhost:8000/api/conversations/' + conversationId + '/');
    const conversation = await response.json();
    console.log(conversation)
    return {"conversation": conversation}
}