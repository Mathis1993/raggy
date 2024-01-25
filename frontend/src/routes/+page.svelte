<script>
    import {Card} from 'flowbite-svelte';
</script>

<Card class="max-w-full">
    <h5 class="mb-2 text-3xl font-bold tracking-tight text-gray-900 dark:text-white"> Dashboard</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
        Welcome to Raggy - your document Copilot.
    </p>
    <hr class="my-4 border-gray-300 dark:border-gray-700">

    <div class="flex space-x-4">
        <Card class="max-w-full" href="/questions">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Ask Questions </h5>
            <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> "We will answer everything</p>
        </Card>
        <Card class="max-w-full" href="/setup">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Setup </h5>
            <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> Setup your project</p>
        </Card>
    </div>
</Card>