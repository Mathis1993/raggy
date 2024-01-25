<script lang="ts">
    import {Activity, ActivityItem, Button, Card} from 'flowbite-svelte';

    /** @type {import('./$types').PageData} */
    export let data;

    console.log(data);

    let activities: [] = data.questions;

</script>

<Card class="max-w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Your Recent Questions</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> This is a list of your most recent
        activity. </p>

    <div class="flex justify-end my-2">
        <Button href="/questions/create">Ask Question</Button>
    </div>

    <Activity class="mt-4">
        <ActivityItem {activities}/>
    </Activity>
</Card>

