<script lang="ts">
    import {
        Button, ButtonGroup,
        Card,
        Checkbox,
        Dropdown,
        Fileupload,
        Helper,
        Input,
        Label,
        Modal, Radio,
        Search,
        Spinner,
        TabItem,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Tabs
    } from "flowbite-svelte";
    import {debounce} from 'lodash';

    import {goto, invalidateAll} from "$app/navigation";
    import {
        createDocumentFromFileUpload,
        createDocumentFromUrl,
        deleteDocument,
        getDocuments,
        retrieveDocument
    } from "./documentService";
    import {
        CheckCircleSolid, ChevronLeftOutline, ChevronRightOutline,
        CloseCircleSolid,
        ExclamationCircleOutline,
        EyeOutline,
        FilterOutline,
        PlusSolid
    } from "flowbite-svelte-icons";
    import {onDestroy, onMount} from "svelte";
    import {page} from "$app/stores";
    import {writable} from "svelte/store";
    import {TableHeader} from "flowbite-svelte-blocks";
    import {list} from "postcss";

    $: documents = $page.data.documents || [];

    let modalVisible: any = {create: false, delete: false, detail: false};
    let createProcessIsRunning = false;
    let documentIdToDelete: number | null = null;
    let documentDetails: ContextDocument | null = null;
    let refreshIntervalId: number;
    let documentURL: string = '';
    let documentName: string = '';
    let errorMessage = writable('');

    // Filtering, Searching and Paginiation
    let selectedDocumentType: string = "";
    let searchQuery = "";
    let documentType = "";
    const debouncedSearch = debounce(filterDocuments, 500);
    let currentPage = 1;
    const pageSize = 1;
    let totalItems = 0;
    let pagesToShow: number[] = [];

    // Fetch the documents for the current page
    async function loadPage() {
        documents = await getDocuments(selectedDocumentType, searchQuery, currentPage);
        totalItems = documents.length; // Update the total number of items
        pagesToShow = Array.from({length: Math.ceil(totalItems / pageSize)}, (_, i) => i + 1); // Calculate the pages to show
    }

    async function loadPreviousPage() {
        if (currentPage > 1) {
            currentPage--;
            await loadPage();
        }
    }

    async function loadNextPage() {
        if (currentPage < pagesToShow.length) {
            currentPage++;
            await loadPage();
        }
    }

    async function goToPage(pageNumber: number) {
        currentPage = pageNumber;
        await loadPage();
    }

    function filterDocuments() {
        let searchParams = new URLSearchParams(window.location.search);
        if (documentType) {
            searchParams.set('type', documentType);
        } else {
            searchParams.delete('type');
        }
        if (searchQuery) {
            searchParams.set('search', searchQuery);
        } else {
            searchParams.delete('search');
        }

        goto(`?` + searchParams.toString(), {replaceState: true});
    }

    function openModal(type: string) {
        modalVisible = {create: false, delete: false, detail: false}; // Reset all
        modalVisible[type] = true;
    }

    function closeModal() {
        modalVisible = {create: false, delete: false, detail: false};
    }


    async function handleCreateFromUrl() {
        createProcessIsRunning = true;
        errorMessage.set(''); // Reset error message on new submission
        try {
            let document = await createDocumentFromUrl(documentURL);
            if (document) {
                documents.push(document);
                await invalidateAll();
                closeModal();
            }
        } catch (error) {
            errorMessage.set(error.message); // Set the error message from the caught error
        } finally {
            createProcessIsRunning = false;
        }
    }


    async function handleCreateFromFileUpload() {
        const fileInput = document.querySelector('#file') as HTMLInputElement;
        errorMessage.set('');
        if (fileInput?.files?.length > 0) {
            try {
                const file = fileInput.files[0];
                const document = await createDocumentFromFileUpload(file, documentName);
                if (document) {
                    documents.push(document);
                    await invalidateAll();
                    closeModal();
                }
            } catch (error) {
                errorMessage.set(error.message);
            }
        }
    }

    async function handleDelete() {
        if (documentIdToDelete !== null) {
            await deleteDocument(documentIdToDelete);
            // TODO: fix invalidation and reloading of the data
            await invalidateAll();
            closeModal();
        }
    }

    async function handleDetailView(documentId: number) {
        if (documentId != null) {
            documentDetails = await retrieveDocument(documentId);
        }
    }


    onMount(() => {
        refreshIntervalId = setInterval(refreshDocuments, 5000);
        loadPage();
    });

    onDestroy(() => {
        clearInterval(refreshIntervalId);
    });

    async function refreshDocuments() {
        for (let i = 0; i < documents.length; i++) {
            if (documents[i].status === 'processing') {
                const updatedDocument = await retrieveDocument(documents[i].id);
                if (updatedDocument.status !== 'processing') {
                    documents[i] = updatedDocument;
                }
            }
        }
    }


</script>

<Card class="max-w-full w-full">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Uploaded Documents</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> This is a list of your uploaded
        documents </p>

    <div class="flex justify-end my-2">
        <Button on:click={() => {openModal("create")}}>
            <PlusSolid class="w-4 h-4 mr-2"></PlusSolid>
            Add Document
        </Button>
    </div>
    <TableHeader headerType="search" divOuterClass="border-0">
        <Search slot="search" size="md" bind:value={searchQuery} on:input={() => {debouncedSearch();}}/>
        <Button color="light" class="ml-2">
            <FilterOutline class="w-4 h-4"></FilterOutline>
            Filter
        </Button>
        <Dropdown class="w-60">
            <ul class="p-2">
                <li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
                    <Radio name="documentType" bind:group={selectedDocumentType} value='all'
                           on:change={() => {documentType="all"; filterDocuments()}}>All
                    </Radio>
                </li>
                <li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
                    <Radio name="documentType" bind:group={selectedDocumentType} value='website'
                           on:change={() => {documentType="website"; filterDocuments()}}>Websites
                    </Radio>
                </li>
                <li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
                    <Radio name="documentType" bind:group={selectedDocumentType} value='text'
                           on:change={() => {documentType="pdf"; filterDocuments()}}>Files
                    </Radio>

                </li>
            </ul>
        </Dropdown>
    </TableHeader>
    <Table hoverable={true}>
        <TableHead>
            <TableHeadCell>Document Name</TableHeadCell>
            <TableHeadCell>URL</TableHeadCell>
            <TableHeadCell>Type</TableHeadCell>
            <TableHeadCell>Status</TableHeadCell>
            <TableHeadCell></TableHeadCell>
        </TableHead>
        <TableBody>
            {#each documents as document}
                <TableBodyRow class={document.status === 'processing' ? 'text-gray-500' : 'text-black'}>
                    <TableBodyCell class={document.status === 'processing' ? 'text-gray-500' : 'text-black'}>
                        {document.title ? document.title.substring(0, 50) : 'No title'}
                    </TableBodyCell>
                    <TableBodyCell class={document.status === 'processing' ? 'text-gray-500' : 'text-black'}>
                        {document.identifier}
                    </TableBodyCell>
                    <TableBodyCell class={document.status === 'processing' ? 'text-gray-500' : 'text-black'}>
                        {document.type}
                    </TableBodyCell>
                    <TableBodyCell>
                        {#if document.status === "processing"}
                            <Spinner/>
                        {:else if document.status === "completed"}
                            <CheckCircleSolid class="text-green-700"/>
                        {:else if document.status === "failed"}
                            <CloseCircleSolid class="text-red-700"/>
                        {/if}
                    </TableBodyCell>
                    <TableBodyCell class="flex items-center justify-between">
                        <Button outline={true}
                                on:click={async () => {openModal("detail"); await handleDetailView(document.id);}}
                                class="border-primary-400 hover:bg-primary-200">
                            <EyeOutline class="text-primary-600"/>
                        </Button>
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
        <div
             class="flex flex-col max-w-full md:flex-row justify-between items-start md:items-center space-y-3 md:space-y-0 p-4">
                <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
                    Showing
                    <span class="font-semibold text-gray-900 dark:text-white">{(currentPage - 1) * pageSize + 1}
                        -{Math.min(currentPage * pageSize, totalItems)}</span>
                    of
                    <span class="font-semibold text-gray-900 dark:text-white">{totalItems}</span>
                </span>
                <ButtonGroup>
                    <Button on:click={loadPreviousPage} disabled={currentPage === 1}>
                        <ChevronLeftOutline size='xs' class='m-1.5'/>
                    </Button>
                    {#each pagesToShow as pageNumber}
                        <Button on:click={() => goToPage(pageNumber)}>{pageNumber}</Button>
                    {/each}
                    <Button on:click={loadNextPage} disabled={currentPage === pagesToShow.length}>
                        <ChevronRightOutline size='xs' class='m-1.5'/>
                    </Button>
                </ButtonGroup>
        </div>
    </Table>
</Card>


<Modal open={modalVisible.create} size="xs" autoclose={false} outsideclose class="w-full">
    <Tabs style="full"
          defaultClass="flex rounded-lg divide-x divide-gray-200 shadow dark:divide-gray-700">
        <TabItem class="w-full" open>
            <span slot="title">URLs</span>
            <form class="flex flex-col space-y-6" on:submit|preventDefault={() => handleCreateFromUrl()}>
                <Label class="space-y-2">
                    <span>URL</span>
                    <Input bind:value={documentURL} type="text" name="url" placeholder="www.company.com" required/>
                    {#if $errorMessage}
                        <p class="text-red-500 text-sm mt-1">{$errorMessage}</p>
                    {/if}
                </Label>
                <Button type="submit" class="w-full1" disabled={createProcessIsRunning}>
                    {#if createProcessIsRunning}
                        <Spinner/>
                    {:else}
                        Add
                    {/if}
                </Button>
            </form>
        </TabItem>
        <TabItem class="w-full">
            <span slot="title">Files</span>
            <form class="flex flex-col space-y-6" on:submit|preventDefault={() => handleCreateFromFileUpload()}>
                <Label for="file" class="pb-2">File Upload</Label>
                <Fileupload id="file" class="mb-2"/>
                <Helper> PDFs or .txt</Helper>
                <Label class="space-y-2 mt-4">
                    <span>Document Name</span>
                    <Input bind:value={documentName} type="text" name="document_name" placeholder="optional"/>
                </Label>
                <Button type="submit" class="w-full1">
                    Add
                </Button>
            </form>
        </TabItem>
    </Tabs>
</Modal>


<Modal open={modalVisible.delete} autoclose={false} outsideclose size="xs">
    <div class="text-center">
        <ExclamationCircleOutline class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200"/>
        <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">Are you sure you want to remove this
            document?</h3>
        <Button on:click={handleDelete} color="red" class="me-2">Yes, I'm sure</Button>
        <Button color="alternative" on:click={() => {closeModal()}}>No, cancel</Button>
    </div>
</Modal>

<Modal title="" open={modalVisible.detail} autoclose outsideclose size="sm">
    <div class="flex justify-between mb-4 rounded-t sm:mb-5">
        <div class="text-lg text-gray-900 md:text-xl dark:text-white">
            <h3 class="font-semibold">{documentDetails ? documentDetails.title : 'Loading...'}</h3>
        </div>
    </div>
    <dl>
        <dt class="mb-2 font-semibold leading-none text-gray-900 dark:text-white">Identifier</dt>
        <dd class="mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400">{documentDetails ? documentDetails.identifier : 'Loading...'}</dd>
        <dt class="mb-2 font-semibold leading-none text-gray-900 dark:text-white">Created At</dt>
        <dd class="mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400">{documentDetails ? documentDetails.created_at : 'Loading...'}</dd>
        <dt class="mb-2 font-semibold leading-none text-gray-900 dark:text-white">Type</dt>
        <dd class="mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400">{documentDetails ? documentDetails.type : 'Loading...'}</dd>
        <dt class="mb-2 font-semibold leading-none text-gray-900 dark:text-white">Status</dt>
        <dd class="mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400">{documentDetails ? documentDetails.status : 'Loading...'}</dd>
        <dt class="mb-2 font-semibold leading-none text-gray-900 dark:text-white">Keywords</dt>
        <dd class="mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400">{documentDetails ? documentDetails.keywords : 'Loading...'}</dd>
    </dl>
    <div class="flex justify-between items-center">
        <div class="flex items-center space-x-3 sm:space-x-4">
            <!--            <Button>-->
            <!--                <svg aria-hidden="true" class="mr-1 -ml-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" /><path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" /></svg>-->
            <!--                Edit-->
            <!--            </Button>-->
        </div>
        <Button color="red" on:click={() => {openModal("delete"); documentIdToDelete = documentDetails.id;}}>
            <svg aria-hidden="true" class="w-5 h-5 mr-1.5 -ml-1" fill="currentColor" viewBox="0 0 20 20"
                 xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                      d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                      clip-rule="evenodd"/>
            </svg>
            Delete
        </Button>
    </div>
</Modal>