import { auth } from "@clerk/nextjs/server";
import { Conversation } from "../types";

const getConversations = async (): Promise<Conversation[]> => {
    try {
        const { userId, getToken, sessionId } = await auth();
        if (!userId) {
            throw new Error("Unauthorized");
        }

        const token = await getToken();
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversations?session_id=${sessionId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        if (!response.ok) {
            throw new Error("Failed to fetch conversations");
        }
        const data = await response.json();
        return data;
    } catch (error) {
        return [];
    }
}
 
export default getConversations;