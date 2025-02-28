import { auth } from "@clerk/nextjs/server";

const getConversationById = async (conversationId: string) => {
    try {
        const { userId, getToken, sessionId } = await auth();
        if (!userId) {
            throw new Error("Unauthorized");
        }

        const token = await getToken();
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversations/${conversationId}?session_id=${sessionId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        
        if (!response.ok) {
            throw new Error("Failed to fetch conversation");
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching conversation:", error);
        return null; // Return null instead of empty array for a single conversation
    }
}
 
export default getConversationById;