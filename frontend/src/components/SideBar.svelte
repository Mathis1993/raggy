<script lang="ts">
    import {Drawer, Sidebar, SidebarGroup, SidebarItem, SidebarWrapper} from "flowbite-svelte";
    import {BookSolid} from "flowbite-svelte-icons";
    import {onMount} from "svelte";
    import {page} from "$app/stores";
    import {goto, invalidateAll} from "$app/navigation";

    let breakPoint: number = 1024;
    let backdrop: boolean = false;
    let activateClickOutside = true;
    let drawerHidden: boolean = false;
    let width = window.innerWidth;

    $: if (width >= breakPoint) {
        drawerHidden = false;
        activateClickOutside = false;
    } else {
        drawerHidden = true;
        activateClickOutside = true;
    }

    onMount(() => {
        if (width >= breakPoint) {
            drawerHidden = false;
            activateClickOutside = false;
        } else {
            drawerHidden = true;
            activateClickOutside = true;
        }
    });
    const toggleSide = () => {
        if (width < breakPoint) {
            drawerHidden = !drawerHidden;
        }
    };

    const toggleDrawer = () => {
        drawerHidden = !drawerHidden;
    };

    $: activeUrl = $page.url.pathname;

    export let data;
    let conversations: Conversation[] = data.conversations;

    let transitionParams = {
        duration: 0,
        disable: true
    };

    let createConversation = async () => {
        console.log('Creating conversation');
        try {
            const response = await fetch('http://localhost:8000/api/conversations/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (!response.ok) {
                console.error('Failed to create conversation');
                return;
            }

            console.log('Conversation created');

            const data = await response.json();
            await goto(`/conversations/${data.id}`, {replaceState: true});
            await invalidateAll();
        } catch (error) {
            console.error('Failed to create conversation', error);
        }
    }
</script>

<Drawer
        {backdrop}
        bind:hidden={drawerHidden}
        bind:activateClickOutside
        width="w-72"
        class="inset-y-[calc(100vh-93vh)] h-full bg-gray-700"
        id="sidebar"
        {transitionParams}
>
    <Sidebar class="w-full">
        <SidebarWrapper class="bg-gray-700 p-0">
            <SidebarGroup class="text-white">
                <SidebarItem class="text-white hover:bg-gray-500"
                             data-sveltekit-reload  label="Start New" on:click={createConversation}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                         class="h-6 w-6">
                        <path d="M12 6v6m0 0v6m0-6h6m-6 0H6" stroke-linecap="round" stroke-linejoin="round"
                              stroke-width="2"></path>
                    </svg>
                </SidebarItem>

                {#each conversations as conversation}
                    <SidebarItem class="text-white hover:bg-gray-500"
                                 label={conversation.name || "Start Conversation..." } data-sveltekit-reload
                                 href={`/conversations/${conversation.id}`} on:click={toggleSide}
                                 active={activeUrl === `conversations/`}>
                    </SidebarItem>
                {/each}

            </SidebarGroup>

            <SidebarGroup border>
                <SidebarItem class="text-white hover:bg-gray-500" label="Documents" href="/documents">
                    <svelte:fragment slot="icon">
                        <BookSolid
                                class="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                    </svelte:fragment>
                </SidebarItem>
            </SidebarGroup>
        </SidebarWrapper>
    </Sidebar>
</Drawer>