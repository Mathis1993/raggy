<script lang="ts">
    import {
        Button,
        Card,
        Dropdown,
        Fileupload,
        Helper,
        Input,
        Label,
        Modal,
        Radio,
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
    import {debounce} from "lodash";

    import {goto, invalidateAll} from "$app/navigation";
    import {
        createDocumentFromFileUpload,
        createDocumentFromUrl,
        deleteDocument,
        getDocuments,
        retrieveDocument
    } from "./documentService";
    import {
        CheckCircleSolid, CheckPlusCircleOutline, CirclePlusOutline,
        CloseCircleSolid,
        DownloadOutline,
        ExclamationCircleOutline,
        EyeOutline,
        FilterOutline,
        PlusSolid
    } from "flowbite-svelte-icons";
    import {onDestroy, onMount} from "svelte";
    import {page} from "$app/stores";
    import {writable} from "svelte/store";
    import {TableHeader} from "flowbite-svelte-blocks";

    $: documents = $page.data.results || [];
    $: hasMore = $page.data.next !== null;
    $: currentPage = $page.data.page || 1;

    let modalVisible: any = {create: false, delete: false, detail: false};
    let createProcessIsRunning = false;
    let documentIdToDelete: number | null = null;
    let documentDetails: ContextDocument | null = null;
    let refreshIntervalId: number;
    let documentURL: string = '';
    let documentName: string = '';
    let errorMessage = writable('');
    const acceptedFileExtensions = ['.pdf', '.txt', '.doc', '.docx'];

    // Filtering, Searching and Paginiation
    let selectedDocumentType: string = "";
    let searchQuery = "";
    let documentType = "";
    const debouncedSearch = debounce(filterDocuments, 500);

    async function loadMoreDocuments() {
        if (!hasMore) return;

        // Already loaded the first page, start from the second page
        currentPage++;
        const response = await getDocuments(documentType, searchQuery, currentPage);
        const newDocuments: ContextDocument[] = response.results;
        const totalDocuments: number = response.count;
        documents = [...documents, ...newDocuments];
        currentPage = response.page;
        if (documents.length >= totalDocuments) {
            hasMore = false;
        }
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

<Card class="max-w-full w-full max-h-[calc(100vh-12vh)] overflow-auto">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"> Uploaded Documents</h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight"> This is a list of your uploaded
        documents </p>
    <TableHeader divOuterClass="border-0">
        <Search name="search" slot="search" size="md" bind:value={searchQuery} on:input={debouncedSearch}/>
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
        <Button on:click={() => {openModal("create")}} class="ml-2">
            <PlusSolid class="w-4 h-4 mr-2"></PlusSolid>
            Add Document
        </Button>
    </TableHeader>
    <Table>
        <TableHead>
            <TableHeadCell>Document Name</TableHeadCell>
            <TableHeadCell>Identifier</TableHeadCell>
            <TableHeadCell>Type</TableHeadCell>
            <TableHeadCell>Status</TableHeadCell>
            <TableHeadCell></TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="scroll-container max-h-96 overflow-y-auto">
            {#each documents as document}
                <TableBodyRow class={document.status === 'processing' ? 'text-gray-500' : 'text-black'}>
                    <TableBodyCell class={document.status === 'processing' ? 'text-gray-500' : 'text-black'}>
                        {document.title ? document.title.substring(0, 40) : 'No title'}
                    </TableBodyCell>
                    <TableBodyCell class={document.status === 'processing' ? 'text-gray-500' : 'text-black'}>
                        {document.identifier ? document.identifier.substring(0, 30) : 'No identifier'}
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

            {#if documents.length === 0}
                <TableBodyRow>
                    <TableBodyCell colspan="5" class="text-center">
                        <p class="text-gray-500 dark:text-gray-400">No documents found</p>
                    </TableBodyCell>
                </TableBodyRow>
            {/if}

            {#if hasMore}
                <TableBodyRow>
                    <TableBodyCell colspan="5" class="text-center">
                        <Button color="alternative" on:click={loadMoreDocuments} class="w-full1">
                            <CirclePlusOutline class="w-4 h-4 mr-2"/>
                            Load More
                        </Button>
                    </TableBodyCell>
                </TableBodyRow>
            {/if}
        </TableBody>
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
                <Fileupload id="file" class="mb-2" accept={acceptedFileExtensions.join(',')}/>
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
            {#if documentDetails && documentDetails.file_url}
                <Button href={documentDetails ? documentDetails.file_url : '#'} target="_blank" color="primary"
                        class="flex items-center space-x-1">
                    <DownloadOutline class="w-5 h-5 mr-1.5 -ml-1" fill="currentColor"/>
                    Download
                </Button>
            {/if}
        </div>
        <Button color="red" on:click={() => {openModal("delete"); documentIdToDelete = documentDetails?.id || null;}}>
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