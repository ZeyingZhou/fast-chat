'use client';

import { useState, useEffect } from "react";
import { format } from "date-fns";
import { useUser } from "@clerk/nextjs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import Image from "next/image";
import { FileIcon, X } from "lucide-react";
import { Message } from "@/types";

interface MessageBoxProps {
  data: Message;
  isLast?: boolean;
}

const MessageBox: React.FC<MessageBoxProps> = ({ 
  data, 
  isLast
}) => {
  const { user } = useUser();
  const [imageModalOpen, setImageModalOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  
  // Use useEffect to handle client-side rendering
  useEffect(() => {
    setMounted(true);
  }, []);

  const isOwn = mounted && user?.id === data?.senderId;
  

  const container = cn(
    'flex gap-3 p-4',
    isOwn && 'justify-end'
  );
  
  const avatar = cn(
    isOwn && 'order-2'
  );
  
  const body = cn(
    'flex flex-col gap-2',
    isOwn && 'items-end'
  );
  
  const message = cn(
    'text-sm w-fit overflow-hidden', 
    isOwn ? 'bg-sky-500 text-white' : 'bg-gray-100', 
    data.files && data.files.length > 0 ? 'rounded-md p-0' : 'rounded-full py-2 px-3'
  );

  return ( 
    <div className={container}>
      <div className={avatar}>
        <Avatar className="size-8 mr-1">
            <AvatarImage className="rounded-md" src={data.sender.image}/>
            <AvatarFallback>
                {data.sender.name?.charAt(0)}
            </AvatarFallback>
        </Avatar>
      </div>
      <div className={body}>
        <div className="flex items-center gap-1">
          <div className="text-sm text-gray-500">
            {data.sender?.name}
          </div>
          <div className="text-xs text-gray-400">
            {format(new Date(data.createdAt), 'p')}
          </div>
        </div>
        <div className={message}>
            <div>{data.body}</div>
          {/* {data.file_url && (
            <div className="mt-2">
              {data.file_type?.startsWith('image/') ? (
                <div className="relative">
                  <Image 
                    alt={data.file_name || "Image"}
                    height="200"
                    width="300"
                    src={data.file_url}
                    className="object-cover rounded-md cursor-pointer"
                    onClick={() => window.open(data.file_url, '_blank')}
                  />
                </div>
              ) : (
                <a 
                  href={data.file_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center p-2 bg-gray-100 rounded-md hover:bg-gray-200 transition"
                >
                  <FileIcon className="h-10 w-10 text-blue-500 mr-2" />
                  <div>
                    <p className="text-sm font-medium">{data.file_name}</p>
                    <p className="text-xs text-gray-500">
                      {data.file_type?.split('/')[1]?.toUpperCase()}
                    </p>
                  </div>
                </a>
              )}
            </div>
          )} */}
        </div>
        {/* {isLast && isOwn && seenList.length > 0 && (
          <div className="
            text-xs 
            font-light 
            text-gray-500
          ">
            {`Seen by ${seenList}`}
          </div>
        )} */}
        {isOwn && data.status && (
          <div className="text-xs text-gray-500 self-end ml-2">
            {data.status === 'sending' && 'Sending...'}
            {data.status === 'sent' && 'Sent'}
            {data.status === 'failed' && (
              <span className="text-red-500">Failed to send</span>
            )}
          </div>
        )}
      </div>
    </div>
   );
}
 
export default MessageBox;
