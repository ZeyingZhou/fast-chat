import { clerkClient } from "@clerk/nextjs/server";
import { auth } from "@clerk/nextjs/server";

const getUsers = async () => {
    try {
        const { userId, getToken, sessionId } = await auth();
        if (!userId) {
            return [];
        }

        const token = await getToken();
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users?session_id=${sessionId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            cache: 'no-store',
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data; // No need to filter here since backend already filters current user
        
    } catch (error) {
        console.error('Failed to fetch users:', error);
        return []; // Return empty array on error, matching get-conversations.ts pattern
    }
};

export default getUsers;