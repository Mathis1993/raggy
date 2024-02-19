<script lang="ts">
    import {Toast} from 'flowbite-svelte';
    import {CheckCircleSolid, CloseCircleSolid, ExclamationCircleSolid} from 'flowbite-svelte-icons';
    import {onMount} from 'svelte';
    import {dismissToast} from "../stores/toastStore.ts";

    export let toast: Toast;

    const autoHideTime = 5000; // 5 seconds

    onMount(() => {
        if (toast.dismissable) {
            setTimeout(() => dismissToast(toast.id), autoHideTime);
        }
    });

    function toastProperties(type: string) {
        switch (type) {
            case 'success':
                return {
                    color: 'green',
                    Icon: CheckCircleSolid,
                    ariaLabel: 'Check icon'
                };
            case 'error':
                return {
                    color: 'red',
                    Icon: CloseCircleSolid,
                    ariaLabel: 'Error icon'
                };
            case 'info':
                return {
                    color: 'orange',
                    Icon: ExclamationCircleSolid,
                    ariaLabel: 'Warning icon'
                };
            default:
                return {
                    color: 'gray',
                    Icon: ExclamationCircleSolid,
                    ariaLabel: 'Info icon'
                };
        }
    }

    const { color, Icon, ariaLabel } = toastProperties(toast.type);
</script>

<Toast {color} class="mb-4 z-0 p-5">
    <svelte:fragment slot="icon">
        <Icon class="w-5 h-5" />
        <span class="sr-only">{ariaLabel}</span>
    </svelte:fragment>
    {toast.message}
</Toast>