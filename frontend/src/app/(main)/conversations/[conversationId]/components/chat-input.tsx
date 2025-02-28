'use client';

import { 
  Send,
  ImageIcon,
  FileTextIcon,
  Paperclip,
  XCircle,
  Smile
} from "lucide-react";
import { 
  FieldValues, 
  SubmitHandler, 
  useForm 
} from "react-hook-form";
import useConversation from "@/hooks/use-conversation";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Image from "next/image";
import { EmojiPopover } from "./emoji-popover";
import getUploadUrl from "@/actions/get-upload-url";

// Define file data interface for better type safety
interface FileData {
  file_url: string;
  file_type: string;
  file_name: string;
  file_size: number;
}

const ChatInput: React.FC = () => {
    const { conversationId } = useConversation();
    const [isUploading, setIsUploading] = useState(false);
    // Store files in a separate state for easier management
    const [attachedFiles, setAttachedFiles] = useState<FileData[]>([]);
    // Add a state to track the message content
    const [messageContent, setMessageContent] = useState('');

    const {
      register,
      handleSubmit,
      setValue,
      getValues,
      formState: {
        errors,
      },
      watch
    } = useForm<FieldValues>({
      defaultValues: {
        message: '',
        files: [] // Changed to array to support multiple files
      }
    });
  
    // Watch the message field to update our state
    const message = watch('message');
    
    // Update messageContent when message changes
    useEffect(() => {
      setMessageContent(message);
    }, [message]);

    const onSubmit: SubmitHandler<FieldValues> = async (data) => {
      setValue('message', '', { shouldValidate: true });
      
      // Get all attached files
      const files = attachedFiles;
      
      // Clear files after sending
      setAttachedFiles([]);
      
      await fetch('/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: data.message,
          files: files, // Send array of file data
          conversationId: conversationId
        }),
      });
    }
  
    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFiles = event.target.files;
      if (!selectedFiles || selectedFiles.length === 0) return;

      setIsUploading(true);
      
      try {
        // Process each file
        for (let i = 0; i < selectedFiles.length; i++) {
          const file = selectedFiles[i];
          
          // First, get a presigned URL from your backend
          const formData = new FormData();
          formData.append('filename', file.name);
          formData.append('content_type', file.type);
          formData.append('conversation_id', conversationId);

          // Use the API endpoint to get the presigned URL
          const response = await fetch('/api/messages/uploadfile', {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            throw new Error('Failed to get presigned URL');
          }

          const { presigned_url, file_url, file_name, file_type } = await response.json();

          // Now upload directly to S3 using the presigned URL
          const uploadResponse = await fetch(presigned_url, {
            method: 'PUT',
            body: file,
            headers: {
              'Content-Type': file.type,
            },
          });

          if (!uploadResponse.ok) {
            throw new Error('Failed to upload file to S3');
          }

          // Add file to attached files array
          setAttachedFiles(prev => [...prev, {
            file_url,
            file_type,
            file_name,
            file_size: file.size
          }]);
        }
        
        // Clear the file input so the same files can be selected again if needed
        event.target.value = '';
      } catch (error) {
        console.error('Error uploading files:', error);
      } finally {
        setIsUploading(false);
      }
    };
  
    const handleEmojiSelect = (emoji: string) => {
      const currentMessage = getValues('message');
      setValue('message', currentMessage + emoji);
    };
    
    const removeAttachment = (index: number) => {
      setAttachedFiles(prev => prev.filter((_, i) => i !== index));
    };
  
    return ( 
      <div 
        className="
          py-4 
          px-4 
          bg-white 
          border-t 
          flex 
          flex-col 
          gap-2 
          w-full
        "
      >
        {/* Files Preview - Display all attached files in a grid */}
        {attachedFiles.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-2">
            {attachedFiles.map((file, index) => (
              <div key={index} className="flex items-center p-2 bg-gray-100 rounded-md gap-2 max-w-fit">
                {file.file_type?.startsWith('image/') ? (
                  <div className="relative h-16 w-16">
                    <Image 
                      src={file.file_url} 
                      alt={file.file_name || "Image"} 
                      fill
                      className="object-cover rounded-md"
                    />
                  </div>
                ) : file.file_type === 'application/pdf' ? (
                  <FileTextIcon className="h-8 w-8 text-red-500" />
                ) : (
                  <Paperclip className="h-8 w-8 text-blue-500" />
                )}
                
                <div className="flex flex-col truncate">
                  <span className="text-sm truncate max-w-[150px]">{file.file_name}</span>
                  <span className="text-xs text-gray-500">
                    {file.file_type?.split('/').pop()?.toUpperCase()}
                  </span>
                </div>
                
                <button 
                  onClick={() => removeAttachment(index)}
                  className="text-gray-500 hover:text-red-500 ml-2"
                  type="button"
                >
                  <XCircle className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
        )}
        
        {/* Message Input */}
        <form 
          onSubmit={handleSubmit(onSubmit)} 
          className="flex items-center gap-2 lg:gap-4 w-full"
        >
          <label className="cursor-pointer">
            <input
              type="file"
              id="fileUpload"
              onChange={handleFileUpload}
              className="hidden"
              multiple  // Enable multiple file selection
            />
            <div className="relative">
              <ImageIcon className={`text-sky-500 ${isUploading ? 'opacity-50' : ''}`} />
              {isUploading && (
                <div className="absolute -top-1 -right-1 h-2 w-2 bg-sky-500 rounded-full animate-ping"></div>
              )}
              {attachedFiles.length > 0 && (
                <div className="absolute -top-1 -right-1 h-4 w-4 bg-sky-500 rounded-full flex items-center justify-center text-white text-xs">
                  {attachedFiles.length}
                </div>
              )}
            </div>
          </label>
          
          {/* Integrated message input */}
          <div className="relative w-full">
            <Input
              id="message"
              autoComplete="message"
              {...register("message", { required: attachedFiles.length === 0 })}
              placeholder="Write a message"
              className="
                text-black
                font-light
                py-2
                px-4
                bg-neutral-100 
                w-full 
                rounded-full
                focus:outline-none
              "
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2">
              <EmojiPopover onEmojiSelect={handleEmojiSelect}>
                <Button 
                  disabled={false}
                  size="sm"
                  variant="ghost"
                  className="rounded-full hover:bg-neutral-200"
                >
                  <Smile className="
                    text-sky-500
                    cursor-pointer
                    hover:text-sky-600
                    transition
                  "/>
                </Button>
              </EmojiPopover>
            </div>
          </div>
          
          <Button 
            type="submit" 
            variant="ghost"
            size="sm"
            className="rounded-full hover:bg-neutral-200"
            disabled={isUploading || (messageContent === '' && attachedFiles.length === 0)}
          >
            <Send className={`
              text-sky-500
              cursor-pointer
              hover:text-sky-600
              transition
              ${(messageContent === '' && attachedFiles.length === 0) ? 'opacity-50' : ''}
            `}/>
          </Button>
        </form>
      </div>
    );
  }
   
export default ChatInput;