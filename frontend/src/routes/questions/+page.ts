/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {

    console.log("Making request to http://localhost:8000/api/questions");
    const response = await fetch('http://localhost:8000/api/questions');
    console.log("Got response from http://localhost:8000/api/questions");
    const questions = await response.json();
    console.log(questions)
    return questions
}