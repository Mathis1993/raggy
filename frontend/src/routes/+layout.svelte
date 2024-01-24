<script>
	import '../app.pcss';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Button } from 'flowbite-svelte';
</script>


<Navbar>
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Edugrade</span>
	</NavBrand>
	<div class="flex md:order-2">
		<Button size="sm">Get started</Button>
		<NavHamburger />
	</div>
</Navbar>

<slot />
