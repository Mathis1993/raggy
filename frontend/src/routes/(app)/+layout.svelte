<script lang="ts">
    import '../../app.pcss';
    import {
        Avatar,
        Button,
        Dropdown,
        DropdownDivider,
        DropdownHeader,
        DropdownItem,
        Navbar,
        NavBrand,
        Sidebar,
        SidebarGroup,
        SidebarItem,
        SidebarWrapper,
        Spinner,
    } from 'flowbite-svelte';
    import {BarsSolid, CirclePlusOutline, FileSearchSolid, OpenBookSolid, PlusSolid} from "flowbite-svelte-icons";
    import {page} from "$app/stores";
    import {onMount} from "svelte";
    import {createConversation, retrieveConversation, retrieveConversations} from "./conversations/conversationService";
    import {getCsrfToken} from '$lib/cookies';
    import {goto} from '$app/navigation';
    import {user} from '../../stores/userStore';
    import {getDocuments} from "./documents/documentService";

    let breakPoint: number = 1024;
    let width: number = typeof window !== 'undefined' ? window.innerWidth : 1024;
    let sidebarVisible: boolean = true;
    $: sidebarVisible = width >= breakPoint;
    $: activeUrl = $page.url.pathname;

    $: conversations = $page.data.conversations.results || [];
    $: hasMore = $page.data.conversations.next !== null;
    $: currentPage = $page.data.conversations.page || 1;
    user.set($page.data.user || {});

    onMount(async () => {
        width = window.innerWidth;
        sidebarVisible = width >= breakPoint;
    });

    function toggleSidebar() {
        if (width < breakPoint) {
            sidebarVisible = !sidebarVisible;
        }
    }

    async function handleLogout() {
        const body = new URLSearchParams({
            'csrfmiddlewaretoken': getCsrfToken(),
        });
        const response = await fetch('http://127.0.0.1:8000/users/logout/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: body,
        });

        if (response.ok) {
            await goto('/login')
        } else {
            const error = await response.json();
            return {status: 'error', error};
        }
    }

    async function loadMoreConversations() {
        if (!hasMore) return;

        // Already loaded the first page, start from the second page
        currentPage++;
        const response = await retrieveConversations(currentPage);
        const newConversations: Conversation[] = response.results;
        const totalConversations: number = response.count;
        conversations = [...conversations, ...newConversations];
        currentPage = response.page;
        if (conversations.length >= totalConversations) {
            hasMore = false;
        }
    }

</script>

<svelte:window bind:innerWidth={width}/>


<header class="flex-none w-full mx-auto bg-white dark:bg-slate-950">
    <Navbar class="fixed flex items-center min-h-10 justify-between h-[calc(100vh-93vh)] bg-gray-700 border-b border-gray-400">
        <div class="absolute left-5 flex">
            {#if width < breakPoint}
                <Button on:click={toggleSidebar} class="bg-gray-700 hover:bg-gray-500 mr-2 px-2 py-1">
                    <BarsSolid class="w-4 h-4"/>
                </Button>
            {/if}
            <NavBrand href="/" class="text-gray-50">
                <span class="self-center whitespace-nowrap text-xl font-semibold">Raggy</span>
                <svg class="w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                     fill="none" viewBox="0 0 24 24">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M16.9 9.7 20 6.6 17.4 4 4 17.4 6.6 20 16.9 9.7Zm0 0L14.3 7M6 7v2m0 0v2m0-2H4m2 0h2m7 7v2m0 0v2m0-2h-2m2 0h2M8 4h0v0h0v0Zm2 2h0v0h0v0Zm2-2h0v0h0v0Zm8 8h0v0h0v0Zm-2 2h0v0h0v0Zm2 2h0v0h0v0Z"/>
                </svg>
            </NavBrand>
        </div>
        <div class="absolute right-5 flex items-center md:order-2">
            <Avatar id="avatar-menu"/>
        </div>
        <Dropdown placement="bottom" triggeredBy="#avatar-menu">
            <DropdownHeader>
                <span class="block text-sm">{`${$user.first_name} ${$user.last_name}`.trim() || ''}</span>
                <span class="block truncate text-sm font-medium">{$user.email}</span>
            </DropdownHeader>
            <DropdownItem href="/settings">Settings</DropdownItem>
            <DropdownDivider/>
            <DropdownItem on:click={handleLogout}>Sign out</DropdownItem>
        </Dropdown>
    </Navbar>
</header>

{#if sidebarVisible}
    <div id="sidebar"
         class="flex flex-col overflow-hidden z-50 px-2 pt-4 dark:bg-gray-800 w-72 fixed start-0 inset-y-[calc(100vh-93vh)] h-full bg-gray-700">
        <Sidebar class="w-full">
            <SidebarWrapper class="bg-gray-700 p-0">
                <SidebarGroup class="text-white flex-grow">
                    <div class="flex items-center justify-between">
                        <h2 class="font-semibold text-lg ml-4">
                            Conversations
                        </h2>
                        <Button size="sm" class="ml-4 bg-gray-700 hover:bg-gray-500" on:click={createConversation}>
                            <PlusSolid class="w-4 h-4"/>
                        </Button>
                    </div>
                    <div class="max-h-[calc(100vh-40vh)] overflow-y-auto">
                        {#if conversations.length === 0}
                            <div class="flex items-center justify-center">
                                No conversations yet
                            </div>
                        {:else}
                            {#each conversations as conversation}
                                <SidebarItem class="text-white hover:bg-gray-500"
                                             label={conversation.name || "Start Conversation..." }
                                             data-sveltekit-reload
                                             href={`/conversations/${conversation.id}`}
                                             on:click={toggleSidebar}
                                             active={activeUrl === `conversations/`}>
                                </SidebarItem>
                            {/each}
                            {#if hasMore}
                                <div class="flex w-full">
                                    <Button color="alternative" on:click={loadMoreConversations} class="bg-gray-700 text-white border-0 w-full">
                                        <CirclePlusOutline class="w-4 h-4 mr-2"/>
                                        Load More
                                    </Button>
                                </div>
                            {/if}
                        {/if}
                    </div>
                </SidebarGroup>

                <SidebarGroup border class="absolute bottom-28 w-full mt-6">
                    <SidebarItem class="text-white hover:bg-gray-500" label="Documents" href="/documents"
                                 on:click={toggleSidebar} active={activeUrl === "/documents"}>
                        <svelte:fragment slot="icon">
                            <FileSearchSolid
                                    class="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                        </svelte:fragment>
                    </SidebarItem>
                    <SidebarItem class="text-white hover:bg-gray-500" label="Information"
                                 href="https://www.llamaindex.ai/" target="_blank" on:click={toggleSidebar}>
                        on:click={toggleSidebar}>
                        <svelte:fragment slot="icon">
                            <OpenBookSolid
                                    class="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                        </svelte:fragment>
                    </SidebarItem>
                </SidebarGroup>
            </SidebarWrapper>
        </Sidebar>
    </div>
{/if}

<div class="flex px-4 mx-auto w-full pt-[calc(100vh-90vh)] h-[calc(100vh-10vh)]">
    <main class="lg:ml-72 w-full mx-auto">
        <slot/>
    </main>
</div>