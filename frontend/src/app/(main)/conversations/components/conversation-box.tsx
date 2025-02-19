import { useRouter } from "next/navigation";
import { FullConversationType } from "../../../../../types";
import { useAuth, useSession } from "@clerk/nextjs";
import useOtherUser from "@/hooks/use-other-user";
import { format } from "date-fns";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { useCallback, useMemo } from "react";
interface ConversationBoxProps {
    data: FullConversationType;
    selected: boolean;
}

const ConversationBox = ({data, selected}: ConversationBoxProps) => {
    const otherUser = useOtherUser(data);
    const router = useRouter();
    const { session } = useSession();
   


  const handleClick = useCallback(() => {
    router.push(`/conversations/${data.id}`);
  }, [data, router]);

  const lastMessage = useMemo(() => {
    const messages = data.messages || [];

    return messages[messages.length - 1];
  }, [data.messages]);

  const userEmail = useMemo(() => session?.user?.emailAddresses[0]?.emailAddress,
  [session?.user?.emailAddresses]);
  
  const hasSeen = useMemo(() => {
    if (!lastMessage) {
      return false;
    }

    const seenArray = lastMessage.seen || [];

    if (!userEmail) {
      return false;
    }

    return seenArray
      .filter((user) => user.email === userEmail).length !== 0;
  }, [userEmail, lastMessage]);

  const lastMessageText = useMemo(() => {
    if (lastMessage?.image) {
      return 'Sent an image';
    }

    if (lastMessage?.body) {
      return lastMessage?.body
    }

    return 'Started a conversation';
  }, [lastMessage]);
  const fallbackName = otherUser.name?.charAt(0).toUpperCase();
    return ( 
        <div
        onClick={handleClick}
        className={cn(`
          w-full 
          relative 
          flex 
          items-center 
          space-x-3 
          p-3 
          hover:bg-neutral-100
          rounded-lg
          transition
          cursor-pointer
          `,
          selected ? 'bg-neutral-100' : 'bg-white'
        )}
      >
        <Avatar className="size-8 mr-1">
            <AvatarImage className="rounded-md" src={otherUser.image} />
            <AvatarFallback>
                {fallbackName}
            </AvatarFallback>
        </Avatar>

        <div className="min-w-0 flex-1">
          <div className="focus:outline-none">
            <span className="absolute inset-0" aria-hidden="true" />
            <div className="flex justify-between items-center mb-1">
              <p className="text-md font-medium text-gray-900">
                {data.users.find((user) => user.id !== userEmail)?.name || otherUser.name}
              </p>
              {lastMessage?.createdAt && (
                <p 
                  className="
                    text-xs 
                    text-gray-400 
                    font-light
                  "
                >
                  {format(new Date(lastMessage.createdAt), 'p')}
                </p>
              )}
            </div>
            <p 
              className={cn(`
                truncate 
                text-xs
                `,
                hasSeen ? 'text-gray-500' : 'text-black font-medium'
              )}>
                {lastMessageText}
              </p>
          </div>
        </div>
      </div>
     );
}
export default ConversationBox;