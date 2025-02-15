'use client';

import { 
  Send,
  ImageIcon 
} from "lucide-react";
import MessageInput from "./message-input";
import { 
  FieldValues, 
  SubmitHandler, 
  useForm 
} from "react-hook-form";
import useConversation from "@/hooks/use-conversation";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const ChatInput: React.FC = () => {
    const { conversationId } = useConversation();
    const [isUploading, setIsUploading] = useState(false);

    const {
      register,
      handleSubmit,
      setValue,
      getValues,
      formState: {
        errors,
      }
    } = useForm<FieldValues>({
      defaultValues: {
        message: ''
      }
    });
  
    const onSubmit: SubmitHandler<FieldValues> = async (data) => {
      setValue('message', '', { shouldValidate: true });
      await fetch('/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...data,
          conversationId: conversationId
        }),
      });
    }
  
    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (!file) return;

      setIsUploading(true);
      try {
        // Create form data for the file
        const formData = new FormData();
        formData.append('file', file);
        formData.append('conversation_id', conversationId);

        // Send to your FastAPI endpoint
        const response = await fetch('/api/messages/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Upload failed');
        }

        // Your FastAPI endpoint will return the S3 URL
        const { image_url } = await response.json();
        
        // Send message with image
        await fetch('/api/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image: image_url,
            conversationId: conversationId
          }),
        });
      } catch (error) {
        console.error('Error uploading file:', error);
        // Add error handling here
      } finally {
        setIsUploading(false);
      }
    }
  
    const handleEmojiSelect = (emoji: string) => {
      const currentMessage = getValues('message');
      setValue('message', currentMessage + emoji);
    };
  
    return ( 
      <div 
        className="
          py-4 
          px-4 
          bg-white 
          border-t 
          flex 
          items-center 
          gap-2 
          lg:gap-4 
          w-full
        "
      >
        <label className="cursor-pointer">
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleFileUpload}
            disabled={isUploading}
          />
          <ImageIcon className={`text-sky-500 ${isUploading ? 'opacity-50' : ''}`} />
        </label>
        <form 
          onSubmit={handleSubmit(onSubmit)} 
          className="flex items-center gap-2 lg:gap-4 w-full"
        >
          <MessageInput 
            id="message" 
            register={register} 
            errors={errors} 
            required 
            placeholder="Write a message"
            onEmojiSelect={handleEmojiSelect}
          />
          <Button 
            type="submit" 
            variant="ghost"
            size="sm"
            className="rounded-full hover:bg-neutral-200"
          >
            <Send className="
                    text-sky-500
                    cursor-pointer
                    hover:text-sky-600
                    transition
                    "/>
          </Button>
        </form>
      </div>
    );
  }
   
export default ChatInput;