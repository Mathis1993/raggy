<script lang="ts">
    import '../app.pcss';
    import {
        Avatar,
        Button,
        Drawer,
        Dropdown,
        DropdownDivider,
        DropdownHeader,
        DropdownItem,
        Navbar,
        NavBrand,
        NavHamburger,
        Sidebar,
        SidebarGroup,
        SidebarItem,
        SidebarWrapper,
    } from 'flowbite-svelte';
    import {BookSolid} from "flowbite-svelte-icons";
    import {onMount} from "svelte";
    import {page} from "$app/stores";
    import {goto, invalidateAll} from "$app/navigation";


    let breakPoint: number = 1024;
    let width: number = 72;
    let activateClickOutside = true;
    let drawerHidden: boolean = false;

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
        transitionType: 'fly',
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


<svelte:window bind:innerWidth={width}/>


<header class="flex-none w-full mx-auto bg-white dark:bg-slate-950">

    <Navbar class="fixed flex items-center h-[calc(100vh-93vh)] bg-gray-700 border-b border-gray-400">
        <Button
                on:click={toggleDrawer}
                class="fixed left-4 bg-gray-700 focus:outline-none whitespace-normal rounded-lg focus:ring-2 p-1.5 focus:ring-gray-400 hover:bg-gray-100 dark:hover:bg-gray-600 m-0 mr-3"
        >
            <NavHamburger class="w-6 h-6"/>
        </Button>
        <NavBrand href="/" class="text-gray-50">
            <span class="self-center whitespace-nowrap text-xl font-semibold">Raggy</span>
            <svg class="w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                 fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M16.9 9.7 20 6.6 17.4 4 4 17.4 6.6 20 16.9 9.7Zm0 0L14.3 7M6 7v2m0 0v2m0-2H4m2 0h2m7 7v2m0 0v2m0-2h-2m2 0h2M8 4h0v0h0v0Zm2 2h0v0h0v0Zm2-2h0v0h0v0Zm8 8h0v0h0v0Zm-2 2h0v0h0v0Zm2 2h0v0h0v0Z"/>
            </svg>
        </NavBrand>
        <div class="flex items-center md:order-2">
            <Avatar id="avatar-menu"/>
        </div>
        <Dropdown placement="bottom" triggeredBy="#avatar-menu">
            <DropdownHeader>
                <span class="block text-sm">Jane Doe</span>
                <span class="block truncate text-sm font-medium">jane@raggy.com</span>
            </DropdownHeader>
            <DropdownItem>Dashboard</DropdownItem>
            <DropdownItem>Settings</DropdownItem>
            <DropdownDivider/>
            <DropdownItem>Sign out</DropdownItem>
        </Dropdown>
    </Navbar>
</header>

<div id="sidebar" class="overflow-y-auto z-50 p-4 dark:bg-gray-800 w-72 fixed start-0 inset-y-[calc(100vh-93vh)] h-full bg-gray-700">
    <Sidebar class="w-full">
        <SidebarWrapper class="bg-gray-700 p-0">
            <SidebarGroup class="text-white">
                <SidebarItem class="text-white hover:bg-gray-500"
                             data-sveltekit-reload label="Start New" on:click={createConversation}>
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
</div>


<div class="flex px-4 mx-auto w-full pt-[calc(100vh-90vh)] h-[calc(100vh-10vh)]">
    <main class="lg:ml-72 w-full mx-auto">
        <slot />
    </main>
</div>