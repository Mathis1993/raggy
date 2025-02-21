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
        deleteDocument, DOCUMENT_API_ENDPOINT,
        getDocuments,
        retrieveDocument
    } from "./documentService";
    import {
        CheckCircleSolid, 
        CheckPlusCircleOutline,
        CirclePlusOutline,
        FilePdfSolid,
        FileSolid,
        CloseCircleSolid,
        DownloadOutline,
        ExclamationCircleOutline,
        EyeOutline,
        FilterOutline,
        PlusSolid,
        DotsVerticalOutline,
        FileSearchSolid,
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
    let selectedTab: 'file' | 'notion' | 'website' = 'file';
    const acceptedFileExtensions = ['.pdf', '.txt', '.doc', '.docx'];

    // Filtering, Searching and Paginiation
    let selectedDocumentType: string = "";
    let searchQuery = "";
    let documentType = "";
    const debouncedSearch = debounce(filterDocuments, 500);

    // Add status color mapping
    const statusColors = {
        'processing': 'text-blue-600',
        'completed': 'text-green-600',
        'failed': 'text-red-600',
        'disabled': 'text-gray-400',
        'archived': 'text-gray-600'
    };

    // Remove the fileTypeIcons mapping and replace with a function
    function getFileIcon(type: string) {
        if (type === 'PDF') {
            return FilePdfSolid;
        } else if (type === 'WEBSITE') {
            return FileSearch;
        } else {
            return FileSearchSolid;
        }
    }

    function formatDateTime(dateString: string, includeSeconds: boolean = false) {
        const date = new Date(dateString);
        return date.toLocaleString(undefined, {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: includeSeconds ? '2-digit' : undefined,
            hour12: false
        });
    }

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
    <div class="flex justify-between items-center mb-4">
        <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Documents</h5>
        <div class="flex items-center gap-2">
            {#if documents.some(doc => doc.status === 'failed')}
                <div class="flex items-center text-sm text-amber-600 bg-amber-50 px-3 py-1 rounded-lg">
                    <ExclamationCircleOutline class="w-4 h-4 mr-1"/>
                    {documents.filter(doc => doc.status === 'failed').length} documents indexing failed
                    <Button size="xs" color="alternative" class="ml-2">RETRY</Button>
                </div>
            {/if}
            <Button on:click={() => {openModal("create")}} class="ml-2">
                <PlusSolid class="w-4 h-4 mr-2"/>
                Add files
            </Button>
        </div>
    </div>

    <TableHeader divClass="mb-4" divOuterClass="border-0">
        <Search name="search" slot="search" size="md" bind:value={searchQuery} on:input={debouncedSearch}/>
        <Button color="light" class="ml-2">
            <FilterOutline class="w-4 h-4"/>
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

    <Table>
        <TableHead>
            <TableHeadCell class="!p-4 w-4">
                <input type="checkbox" class="rounded border-gray-300">
            </TableHeadCell>
            <TableHeadCell>Name</TableHeadCell>
            <TableHeadCell>Upload Time</TableHeadCell>
            <TableHeadCell>Status</TableHeadCell>
            <TableHeadCell class="w-20"></TableHeadCell>
        </TableHead>
        <TableBody>
            {#each documents as document}
                <TableBodyRow>
                    <TableBodyCell class="!p-4">
                        <input type="checkbox" class="rounded border-gray-300">
                    </TableBodyCell>
                    <TableBodyCell>
                        <div class="flex items-center">
                            <div class="p-2 bg-gray-100 rounded-lg mr-3">
                                <svelte:component this={getFileIcon(document.type)} class="w-5 h-5 text-gray-600" />
                            </div>
                            <div>
                                <p class="font-medium text-gray-900">{document.title || 'Untitled'}</p>
                                <p class="text-sm text-gray-500">{document.identifier}</p>
                            </div>
                        </div>
                    </TableBodyCell>
                    <TableBodyCell>
                        {formatDateTime(document.created_at)}
                    </TableBodyCell>
                    <TableBodyCell>
                        <div class="flex items-center">
                            {#if document.status === "PROCESSING"}
                                <div class="flex items-center text-blue-600">
                                    <Spinner size="sm" class="mr-2"/>
                                    <span class="text-sm font-medium">Indexing...</span>
                                </div>
                            {:else if document.status === "COMPLETED"}
                                <div class="flex items-center text-green-600">
                                    <CheckCircleSolid class="w-4 h-4 mr-2"/>
                                    <span class="text-sm font-medium">Available</span>
                                </div>
                            {:else if document.status === "FAILED"}
                                <div class="flex items-center text-red-600">
                                    <CloseCircleSolid class="w-4 h-4 mr-2"/>
                                    <span class="text-sm font-medium">Error</span>
                                </div>
                            {:else if document.status === "DISABLED"}
                                <div class="flex items-center text-gray-400">
                                    <span class="text-sm font-medium">Disabled</span>
                                </div>
                            {:else if document.status === "ARCHIVED"}
                                <div class="flex items-center text-gray-600">
                                    <span class="text-sm font-medium">Archived</span>
                                </div>
                            {/if}
                        </div>
                    </TableBodyCell>
                    <TableBodyCell>
                        <div class="flex items-center justify-end gap-2">
                            <Button outline={true} size="sm"
                                    on:click={async () => {openModal("detail"); await handleDetailView(document.id);}}
                                    class="!p-2 border-gray-200">
                                <EyeOutline class="w-4 h-4 text-gray-500"/>
                            </Button>
                            <Button outline={true} size="sm" class="!p-2 border-gray-200">
                                <DotsVerticalOutline class="w-4 h-4 text-gray-500"/>
                            </Button>
                        </div>
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
                        <Button color="alternative" on:click={loadMoreDocuments}>
                            <CirclePlusOutline class="w-4 h-4 mr-2"/>
                            Load More
                        </Button>
                    </TableBodyCell>
                </TableBodyRow>
            {/if}
        </TableBody>
    </Table>
</Card>


<Modal open={modalVisible.create} size="md" autoclose={false} outsideclose class="w-full">
    <div class="p-4">
        <h3 class="text-xl font-semibold mb-6">Choose data source</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <!-- File Upload Option -->
            <button class="flex items-center p-4 border-2 border-primary-100 rounded-lg hover:bg-primary-50 transition-colors {selectedTab === 'file' ? 'border-primary-500 bg-primary-50' : ''}"
                    on:click={() => selectedTab = 'file'}>
                <div class="p-2 bg-primary-100 rounded-lg mr-3">
                    <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                </div>
                <span class="text-sm font-medium">Import from text file</span>
            </button>

            <!-- Notion Option -->
            <button class="flex items-center p-4 border-2 border-primary-100 rounded-lg hover:bg-primary-50 transition-colors {selectedTab === 'notion' ? 'border-primary-500 bg-primary-50' : ''}"
                    on:click={() => selectedTab = 'notion'}>
                <div class="p-2 bg-primary-100 rounded-lg mr-3">
                    <svg class="w-6 h-6 text-primary-600" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M4.459 4.208c.746.606 1.026.56 2.428.466l13.215-.793c.28 0 .047-.28-.046-.326L17.86 1.968c-.42-.326-.981-.7-2.055-.607L3.01 2.295c-.466.046-.56.28-.374.466zm.793 3.08v13.904c0 .747.373 1.027 1.214.98l14.523-.84c.841-.046.935-.56.935-1.167V6.354c0-.606-.233-.933-.748-.887l-15.177.887c-.56.047-.747.327-.747.933zm14.337.745c.093.42 0 .84-.42.888l-.7.14v10.264c-.608.327-1.168.514-1.635.514-.748 0-.935-.234-1.495-.933l-4.577-7.186v6.952L12.21 19s0 .84-1.168.84l-3.222.186c-.093-.186 0-.653.327-.746l.84-.233V9.854L7.822 9.76c-.094-.42.14-1.026.793-1.073l3.456-.233 4.764 7.279v-6.44l-1.215-.139c-.093-.514.28-.887.747-.933zM1.936 1.035l13.31-.98c1.634-.14 2.055-.047 3.082.7l4.249 2.986c.7.513.934.653.934 1.213v16.378c0 1.026-.373 1.634-1.68 1.726l-15.458.934c-.98.047-1.448-.093-1.962-.747l-3.129-4.06c-.56-.747-.793-1.306-.793-1.96V2.667c0-.839.374-1.54 1.447-1.632z"/>
                    </svg>
                </div>
                <span class="text-sm font-medium">Sync from Notion</span>
            </button>

            <!-- Website Option -->
            <button class="flex items-center p-4 border-2 border-primary-100 rounded-lg hover:bg-primary-50 transition-colors {selectedTab === 'website' ? 'border-primary-500 bg-primary-50' : ''}"
                    on:click={() => selectedTab = 'website'}>
                <div class="p-2 bg-primary-100 rounded-lg mr-3">
                    <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                </div>
                <span class="text-sm font-medium">Sync from web site</span>
            </button>
        </div>

        {#if selectedTab === 'file'}
            <div class="mt-6">
                <div class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
                     on:click={() => {
                        const fileInput = document.getElementById('file');
                        if (fileInput) fileInput.click();
                     }}
                     on:dragover|preventDefault
                     on:drop|preventDefault={(e) => {
                        const files = e.dataTransfer?.files;
                        if (files?.length > 0) {
                            const fileInput = document.getElementById('file');
                            if (fileInput instanceof HTMLInputElement) {
                                fileInput.files = files;
                                // Trigger the change event manually since we're setting files programmatically
                                const event = new Event('change', { bubbles: true });
                                fileInput.dispatchEvent(event);
                            }
                        }
                     }}>
                    <div class="flex flex-col items-center justify-center pt-5 pb-6">
                        <svg class="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        <p class="mb-2 text-sm text-gray-500">
                            <span class="font-semibold">Click to upload</span> or drag and drop
                        </p>
                        <p class="text-xs text-gray-500">Supports txt, html, markdown, pdf, xlsx, csv and JSONL files (text type). Max 15MB each.</p>
                    </div>
                    <Fileupload id="file" class="hidden" accept={acceptedFileExtensions.join(',')} on:change={(e) => {
                        const fileInput = e.target;
                        if (fileInput instanceof HTMLInputElement && fileInput.files?.[0]) {
                            documentName = documentName || fileInput.files[0].name;
                        }
                    }}/>
                </div>
                <div class="mt-4">
                    <Label class="space-y-2">
                        <span>Document Name (optional)</span>
                        <Input bind:value={documentName} type="text" name="document_name" placeholder="Enter a name for your document"/>
                    </Label>
                </div>
                {#if $errorMessage}
                    <div class="mt-4 p-4 text-sm text-red-800 rounded-lg bg-red-50" role="alert">
                        {$errorMessage}
                    </div>
                {/if}
                <div class="mt-6 flex justify-end">
                    <Button type="button" color="alternative" class="mr-2" on:click={() => closeModal()}>Cancel</Button>
                    <Button type="submit" on:click={() => handleCreateFromFileUpload()} disabled={createProcessIsRunning}>
                        {#if createProcessIsRunning}
                            <Spinner size="sm" class="mr-2"/>
                            Processing
                        {:else}
                            Upload Document
                        {/if}
                    </Button>
                </div>
            </div>
        {:else if selectedTab === 'website'}
            <div class="mt-6">
                <Label class="space-y-2">
                    <span>Website URL</span>
                    <Input bind:value={documentURL} type="text" name="url" placeholder="https://www.example.com" required/>
                </Label>
                {#if $errorMessage}
                    <div class="mt-4 p-4 text-sm text-red-800 rounded-lg bg-red-50" role="alert">
                        {$errorMessage}
                    </div>
                {/if}
                <div class="mt-6 flex justify-end">
                    <Button type="button" color="alternative" class="mr-2" on:click={() => closeModal()}>Cancel</Button>
                    <Button type="submit" on:click={() => handleCreateFromUrl()} disabled={createProcessIsRunning}>
                        {#if createProcessIsRunning}
                            <Spinner size="sm" class="mr-2"/>
                            Processing
                        {:else}
                            Add URL
                        {/if}
                    </Button>
                </div>
            </div>
        {:else if selectedTab === 'notion'}
            <div class="mt-6">
                <div class="p-4 text-sm text-gray-800 rounded-lg bg-gray-50">
                    Coming soon! Notion integration will be available in a future update.
                </div>
            </div>
        {/if}
    </div>
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

<Modal title="" open={modalVisible.detail} autoclose outsideclose size="md">
    <div class="p-6">
        <div class="flex items-start gap-4 mb-6">
            <div class="p-3 bg-gray-100 rounded-lg">
                <svelte:component this={getFileIcon(documentDetails?.type || 'txt')} class="w-6 h-6 text-gray-600" />
            </div>
            <div>
                <h3 class="text-xl font-semibold text-gray-900">{documentDetails?.title || 'Loading...'}</h3>
                <p class="text-sm text-gray-500">{documentDetails?.identifier || 'Loading...'}</p>
            </div>
        </div>

        <div class="space-y-4">
            <div class="flex items-center justify-between py-3 border-b border-gray-200">
                <span class="text-sm font-medium text-gray-500">Status</span>
                <div class="flex items-center">
                    {#if documentDetails?.status === "PROCESSING"}
                        <div class="flex items-center text-blue-600">
                            <Spinner size="sm" class="mr-2"/>
                            <span class="text-sm font-medium">Indexing...</span>
                        </div>
                    {:else if documentDetails?.status === "COMPLETED"}
                        <div class="flex items-center text-green-600">
                            <CheckCircleSolid class="w-4 h-4 mr-2"/>
                            <span class="text-sm font-medium">Available</span>
                        </div>
                    {:else if documentDetails?.status === "FAILED"}
                        <div class="flex items-center text-red-600">
                            <CloseCircleSolid class="w-4 h-4 mr-2"/>
                            <span class="text-sm font-medium">Error</span>
                        </div>
                    {:else if documentDetails?.status === "DISABLED"}
                        <div class="flex items-center text-gray-400">
                            <span class="text-sm font-medium">Disabled</span>
                        </div>
                    {:else if documentDetails?.status === "ARCHIVED"}
                        <div class="flex items-center text-gray-600">
                            <span class="text-sm font-medium">Archived</span>
                        </div>
                    {/if}
                </div>
            </div>

            <div class="flex items-center justify-between py-3 border-b border-gray-200">
                <span class="text-sm font-medium text-gray-500">Type</span>
                <span class="text-sm text-gray-900">{documentDetails?.type || 'Loading...'}</span>
            </div>

            <div class="flex items-center justify-between py-3 border-b border-gray-200">
                <span class="text-sm font-medium text-gray-500">Upload Time</span>
                <span class="text-sm text-gray-900">{documentDetails ? formatDateTime(documentDetails.created_at, true) : 'Loading...'}</span>
            </div>
        </div>

        <div class="flex justify-end items-center gap-3 mt-6">
            {#if documentDetails && documentDetails.type !== 'website'}
                <Button href="{DOCUMENT_API_ENDPOINT}download/{documentDetails.id}" target="_blank" color="primary"
                        class="flex items-center">
                    <DownloadOutline class="w-4 h-4 mr-2"/>
                    Download
                </Button>
            {/if}
            <Button color="red" class="flex items-center" on:click={() => {openModal("delete"); documentIdToDelete = documentDetails?.id || null;}}>
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Delete
            </Button>
        </div>
    </div>
</Modal>