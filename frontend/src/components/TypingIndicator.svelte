<script lang="ts">
</script>

<div class="flex gap-3 mb-6">
    <div class="w-8 h-8 flex-shrink-0 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-300 mt-1">
        A
    </div>
    
    <div class="flex-1 max-w-[85%]">
        <div class="rounded-lg px-4 py-3 bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
            <div class="flex items-center gap-1">
                <div class="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-typing-1"></div>
                <div class="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-typing-2"></div>
                <div class="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-typing-3"></div>
            </div>
        </div>
    </div>
</div>

<style>
    @keyframes typing {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }

    :global(.animate-typing-1) {
        animation: typing 1s infinite;
    }

    :global(.animate-typing-2) {
        animation: typing 1s infinite;
        animation-delay: 0.2s;
    }

    :global(.animate-typing-3) {
        animation: typing 1s infinite;
        animation-delay: 0.4s;
    }
</style> 