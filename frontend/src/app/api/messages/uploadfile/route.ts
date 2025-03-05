import { NextResponse } from "next/server";
import getUploadUrl from "@/actions/get-upload-url";
import { auth } from "@clerk/nextjs/server";

export async function POST(request: Request) {
  try {
    // Verify authentication
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Get form data
    const formData = await request.formData();
    const filename = formData.get("filename") as string;
    const contentType = formData.get("content_type") as string;
    const conversationId = formData.get("conversation_id") as string;

    // Use the existing action to generate the upload URL
    const result = await getUploadUrl(filename, contentType, conversationId);

    // Return the result
    return NextResponse.json(result);
  } catch (error) {
    console.error("Error generating presigned URL:", error);
    
    // Check if it's an unauthorized error
    if (error instanceof Error && error.message === "Unauthorized") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    
    return NextResponse.json(
      { error: "Failed to generate upload URL" },
      { status: 500 }
    );
  }
}