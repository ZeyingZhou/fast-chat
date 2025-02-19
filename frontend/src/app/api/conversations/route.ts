import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";

export async function POST(request: Request) {
    try {
        const { userId: currentUserId, getToken, sessionId } = await auth();
        if (!currentUserId) {
            throw new Error("Unauthorized");
        }
        const body = await request.json();
        const { userId } = body;  // Extract otherUserId from request body

        const token = await getToken();
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversations?session_id=${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({userId})
        });
        if (!response.ok) {
            throw new Error("Failed to fetch conversations");
        }
        const conversationData = await response.json();
        return NextResponse.json(conversationData);
    } catch (error) {
        return new NextResponse('Internal Error', { status: 500 });
    }
} 