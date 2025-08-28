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
    } from 'flowbite-svelte';
    import {
        BarsSolid, 
        ChervonDoubleLeftSolid,
        ChervonDoubleRightSolid,
        MessagesOutline,
        BookOpenOutline,
        QuestionCircleOutline,
        AdjustmentsVerticalOutline,
        ArrowLeftToBracketOutline,
    } from "flowbite-svelte-icons";
    import {page} from "$app/stores";
    import {onMount, tick} from "svelte";
    import {createConversation, retrieveConversations} from "./conversations/conversationService";
    import {getCsrfToken} from '$lib/cookies';
    import {goto} from '$app/navigation';
    import {user} from '../../stores/userStore';
    import ToastModal from "../../components/ToastModalSection.svelte";
    import { fetchFromBackend } from '$lib/fetch';

    let breakPoint: number = 1024;
    let width: number = typeof window !== 'undefined' ? window.innerWidth : 1024;
    let sidebarVisible: boolean = true;
    let sidebarCollapsed: boolean = false;
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

    function toggleCollapse() {
        sidebarCollapsed = !sidebarCollapsed;
    }

    async function handleLogout() {
        const response = await fetchFromBackend('http://127.0.0.1:8000/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
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
    <Navbar class="fixed flex items-center min-h-16 max-h-16 justify-between bg-gray-800 border-b border-gray-700">
        <div class="absolute left-5 flex items-center">
            {#if width < breakPoint}
                <Button on:click={toggleSidebar} class="bg-gray-800 hover:bg-gray-700 mr-2 px-2 py-1">
                    <BarsSolid class="w-4 h-4"/>
                </Button>
            {/if}
            <NavBrand href="/conversations" class="text-gray-50 flex items-center">
                <svg class="w-8 h-8 mr-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                     fill="none" viewBox="0 0 24 24">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M16.9 9.7 20 6.6 17.4 4 4 17.4 6.6 20 16.9 9.7Zm0 0L14.3 7M6 7v2m0 0v2m0-2H4m2 0h2m7 7v2m0 0v2m0-2h-2m2 0h2M8 4h0v0h0v0Zm2 2h0v0h0v0Zm2-2h0v0h0v0Zm8 8h0v0h0v0Zm-2 2h0v0h0v0Zm2 2h0v0h0v0Z"/>
                </svg>
                <span class="self-center whitespace-nowrap text-2xl font-semibold">Raggy</span>
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
            <DropdownItem href="/settings">Account Settings</DropdownItem>
            <DropdownDivider/>
            <DropdownItem on:click={handleLogout}>Sign out</DropdownItem>
        </Dropdown>
    </Navbar>
</header>

{#if sidebarVisible}
    <div id="sidebar"
         class="flex flex-col overflow-hidden z-50 dark:bg-gray-800 {sidebarCollapsed ? 'w-16' : 'w-72'} fixed start-0 top-16 h-[calc(100vh-4rem)] bg-gray-800 transition-all duration-300">
        <Sidebar class="w-full flex flex-col h-full">
            <SidebarWrapper class="bg-gray-800 p-0 flex flex-col h-full">
                <SidebarGroup class="text-white flex-grow">
                    <SidebarItem class="text-gray-300 hover:bg-gray-700 px-3 py-3 my-1" href="/conversations"
                                active={activeUrl.includes("/conversations")} label={sidebarCollapsed ? '' : 'Chat'}>
                        <MessagesOutline class="w-6 h-6" slot="icon"/>
                    </SidebarItem>

                    <SidebarItem class="text-gray-300 hover:bg-gray-700 px-3 py-3 my-1" href="/documents"
                                active={activeUrl.includes("/documents")} label={sidebarCollapsed ? '' : 'Knowledge Base'}>
                        <BookOpenOutline class="w-6 h-6" slot="icon"/>
                    </SidebarItem>

                    <SidebarItem class="text-gray-300 hover:bg-gray-700 px-3 py-3 my-1" href="/faq"
                                active={activeUrl.includes("/faq")} label={sidebarCollapsed ? '' : 'FAQ'}>
                        <QuestionCircleOutline class="w-6 h-6" slot="icon"/>
                    </SidebarItem>

                    <SidebarItem class="text-gray-300 hover:bg-gray-700 px-3 py-3 my-1" href="/settings"
                                active={activeUrl.includes("/settings")} label={sidebarCollapsed ? '' : 'Project Settings'}>
                        <AdjustmentsVerticalOutline class="w-6 h-6" slot="icon"/>
                    </SidebarItem>
                </SidebarGroup>
                <div class="mt-auto">
                    <div class="px-3 py-2">
                        <Button
                            class="w-full bg-gray-700 hover:bg-gray-600 flex justify-center"
                            size="xs"
                            on:click={toggleCollapse}
                        >
                            {#if sidebarCollapsed}
                                <ChervonDoubleRightSolid class="w-4 h-4"/>
                            {:else}
                                <ChervonDoubleLeftSolid class="w-4 h-4"/>
                            {/if}
                        </Button>
                    </div>
                </div>
            </SidebarWrapper>
        </Sidebar>
    </div>
{/if}

<div class="flex mx-auto w-full pt-16 h-screen">
    <main class="{sidebarVisible ? (sidebarCollapsed ? 'lg:ml-16' : 'lg:ml-72') : ''} w-full mx-auto transition-all duration-300">
        <slot/>
    </main>
    <ToastModal/>
</div>
