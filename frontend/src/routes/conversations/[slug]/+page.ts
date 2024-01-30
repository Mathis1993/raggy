

export async function load({ params }: { params: any }) {
    console.log("Making request to http://localhost:8000/api/questions");
    let questionId: number = params.slug
    const response = await fetch('http://localhost:8000/api/questions/' + questionId + '/');
    const question = await response.json();
    console.log(question)
    return question
}