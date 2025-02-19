// types.ts

// Base User interface (from Clerk + additional fields)
export interface User {
    id: string;          // Clerk user ID
    email: string;       // From Clerk
    username: string;    // From Clerk
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
    body: string | null;        // Optional message text
    image: string | null;       // Optional message image
    senderId: string;           // Clerk user ID of sender
    conversationId: string;     // ID of parent conversation
    createdAt: string;
    seenBy?: {                 // List of users who've seen the message
        userId: string;
        seenAt: string;
    }[];
}

// Extended Message with relationships
export interface FullMessageType extends Message {
    sender: User;              // Denormalized sender info
    seen: User[];             // List of users who've seen the message
}

// Base Conversation interface
export interface Conversation {
    id: string;
    name: string | null;       // Optional conversation name
    isGroup: boolean;          // Whether this is a group conversation
    createdAt: string;
    lastMessageAt: string;     // Timestamp of most recent message
    lastMessage?: {            // Denormalized last message for preview
        id: string;
        body: string | null;
        senderId: string;
        createdAt: string;
    };
    userIds: {            // Denormalized participant info
        id: string;
    }[];
}

// Extended Conversation with full relationships
export interface FullConversationType extends Conversation {
    users: User[];            // Full user objects of participants
    messages: FullMessageType[];  // Full message objects with sender/seen info
}

// API Response types