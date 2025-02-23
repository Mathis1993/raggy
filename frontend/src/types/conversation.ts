export type Conversation = {
    id: number;
    name: string;
    created_at: string;
    status: string;
    messages: Message[];
}

export type Message = {
    id: number;
    text: string;
    created_at: string;
    conversation: Conversation;
    is_user_message: boolean;
    sources: MessageSource[];
}

export type MessageSource = {
    document: ContextDocument;
    excerpt: string;
}

export type ContextDocument = {
    id: number;
    title: string;
    type: string;
}