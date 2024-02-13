type Conversation = {
    id: number;
    name: string;
    created_at: string;
    status: string;
    messages: Message[];
}

type Message = {
    id: number;
    text: string;
    created_at: string;
    conversation: Conversation;
    is_user_message: boolean;
    sources: ContextDocument[];
}