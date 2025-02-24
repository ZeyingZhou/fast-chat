// types.ts

// Base User interface (from Clerk + additional fields)
export interface User {
    id: string;          // Clerk user ID
    email: string;       // From Clerk    // From Clerk
    name: string;    // From Clerk
    image: string;       // From Clerk
}

export interface DatabaseUser extends User {
    createdAt: string;
    updatedAt: string;
    conversationIds: string[];
    seenMessageIds: string[];
}

// Base Message interface
export interface Message {
    id: string;
    conversationId: string;
    senderId: string;
    body: string | null;
    image?: string | null;
    createdAt: string;
    sender: User;
}

// Base Conversation interface
export interface Conversation {
    id: string;
    name: string | null;       // Optional conversation name
    isGroup: 'true' | 'false';        // Whether this is a group conversation
    createdAt: string;
    lastMessageAt: string;     // Timestamp of most recent message
    users: User[];
}

