import { Message } from "@/types";
import { auth } from "@clerk/nextjs/server";

const getMessages = async (conversationId: string): Promise<Message[]> => {
    try {
        const { getToken, sessionId } = await auth();
        const token = await getToken();
        
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/messages/${conversationId}?session_id=${sessionId}`, 
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
            }
        );
        
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching messages:", error);
        return [];
    }
}

export default getMessages;