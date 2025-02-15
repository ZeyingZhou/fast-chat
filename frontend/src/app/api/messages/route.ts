import { NextResponse } from "next/server";


export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in messages API:', error);
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
