'use client';

import { useState } from "react";
import { format } from "date-fns";
import { useUser } from "@clerk/nextjs";
import { FullMessageType } from "../../../../../types";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import Image from "next/image";
interface MessageBoxProps {
  data: FullMessageType;
  isLast?: boolean;
}

const MessageBox: React.FC<MessageBoxProps> = ({ 
  data, 
  isLast
}) => {
  const { user } = useUser();
  const [imageModalOpen, setImageModalOpen] = useState(false);

  const isOwn = user?.id === data?.senderId;
  
  // Get list of users who've seen the message (excluding sender)
  const seenList = (data.seenBy || [])
    .filter((seen) => seen.userId !== data.senderId)
    .map((seen) => seen.userId)
    .join(', ');

  // Dynamic classes based on message ownership and type
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
    data.image ? 'rounded-md p-0' : 'rounded-full py-2 px-3'
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
          {data.image ? (
            <Image
              alt="Image"
              height="288"
              width="288"
              onClick={() => setImageModalOpen(true)} 
              src={data.image} 
              className="
                object-cover 
                cursor-pointer 
                hover:scale-110 
                transition 
                translate
              "
            />
          ) : (
            <div>{data.body}</div>
          )}
        </div>
        {isLast && isOwn && seenList.length > 0 && (
          <div className="
            text-xs 
            font-light 
            text-gray-500
          ">
            {`Seen by ${seenList}`}
          </div>
        )}
      </div>
    </div>
   );
}
 
export default MessageBox;
