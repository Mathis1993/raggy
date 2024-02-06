<script>
    import {
        Avatar,
        Button,
        Dropdown,
        DropdownDivider,
        DropdownHeader, DropdownItem,
        Navbar,
        NavBrand,
        NavHamburger
    } from "flowbite-svelte";

    export let toggleDrawer;

</script>

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