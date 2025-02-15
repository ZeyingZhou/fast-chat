import { auth } from "@clerk/nextjs/server";

const getMessages = async (conversationId: string) => {
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/messages/${conversationId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error("Failed to fetch messages");
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching messages:", error);
        return [];
    }
}

export default getMessages;