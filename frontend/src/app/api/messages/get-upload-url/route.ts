import { NextResponse } from "next/server";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { v4 as uuidv4 } from "uuid";
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

    // Generate unique filename
    const fileExtension = filename.split('.').pop();
    const newFilename = `${uuidv4()}.${fileExtension}`;
    
    // Create S3 key
    const s3Key = `conversations/${conversationId}/${newFilename}`;

    // Initialize S3 client
    const s3Client = new S3Client({
      region: process.env.AWS_REGION!,
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
      },
    });

    // Create command for S3 PUT operation
    const command = new PutObjectCommand({
      Bucket: process.env.AWS_BUCKET_NAME!,
      Key: s3Key,
      ContentType: contentType,
    });

    // Generate presigned URL
    const presignedUrl = await getSignedUrl(s3Client, command, { expiresIn: 3600 });

    // Generate final file URL
    const fileUrl = `https://${process.env.AWS_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${s3Key}`;

    // Return presigned URL and file metadata
    return NextResponse.json({
      presigned_url: presignedUrl,
      file_url: fileUrl,
      file_name: filename,
      file_type: contentType,
    });
  } catch (error) {
    console.error("Error generating presigned URL:", error);
    return NextResponse.json(
      { error: "Failed to generate upload URL" },
      { status: 500 }
    );
  }
}