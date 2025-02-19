import { NextResponse } from "next/server";


export async function POST(request: Request) {
  try {
    // Forward the FormData directly to FastAPI
    const formData = await request.formData();
    
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/messages/upload`, {
      method: 'POST',
      body: formData, // FastAPI will handle the multipart/form-data
    });

    if (!response.ok) {
      throw new Error('Failed to upload file');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in upload API:', error);
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
