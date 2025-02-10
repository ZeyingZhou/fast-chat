import { clerkClient } from "@clerk/nextjs/server";
import { auth } from "@clerk/nextjs";

const getUsers = async () => {
    try {
        const { userId } = auth();
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            // Adding cache control if needed
            cache: 'no-store', // or 'force-cache' if you want to cache
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        // Filter out the current user from the results
        return data.filter((user: any) => user.id !== userId);
        
    } catch (error) {
        console.error('Failed to fetch users:', error);
        throw error; // Re-throw to handle in the component
    }
};

export default getUsers;