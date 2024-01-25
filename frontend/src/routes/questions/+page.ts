/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: any }) {

    console.log("Making request to http://localhost:8000/api/questions");
    const response = await fetch('http://localhost:8000/api/questions');
    console.log("Got response from http://localhost:8000/api/questions");
    console.log(response);
    const questions = await response.json();


    // rename the fields: question -> title, answer -> text, created_at -> date
    return {
        questions: questions.questions.map((question: any) => ({
            title: question.question,
            text: question.answer,
            date: question.created_at,
        }))
    }
}