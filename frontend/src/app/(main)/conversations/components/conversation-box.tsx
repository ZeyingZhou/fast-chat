import { useRouter } from "next/navigation";
import { Conversation } from "../../../../types";
import { useAuth, useSession } from "@clerk/nextjs";
import useOtherUser from "@/hooks/use-other-user";
import { format } from "date-fns";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { useCallback, useMemo } from "react";
import AvatarGroup from "@/components/avatar-group";
import AvatarUser from "@/components/avatar-user";
interface ConversationBoxProps {
    conversation: Conversation;
    selected: boolean;
}

const ConversationBox = ({conversation, selected}: ConversationBoxProps) => {
  const otherUser = useOtherUser(conversation);
  const router = useRouter();
   
  const handleClick = useCallback(() => {
    router.push(`/conversations/${conversation.id}`);
  }, [conversation, router]);

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
        {conversation.isGroup === "true" ? (
          <AvatarGroup users={conversation.users} />
        ): (
          <AvatarUser user={otherUser} />
        )}
  
        <div className="min-w-0 flex-1">
          <div className="focus:outline-none">
            <span className="absolute inset-0" aria-hidden="true" />
            <div className="flex justify-between items-center mb-1">
            <p className="text-md font-medium text-gray-900">
              {conversation.name || otherUser.name}
            </p>
            <p 
                className="
                  text-xs 
                  text-gray-400 
                  font-light
                "
              >
                {format(new Date(conversation.lastMessageAt), 'p')}
              </p>
            </div>
          </div>
        </div>
      </div>
     );
}
export default ConversationBox;