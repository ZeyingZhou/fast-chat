import { useRouter } from "next/navigation";
import { Conversation } from "../../../../types";
import { useAuth, useSession } from "@clerk/nextjs";
import useOtherUser from "@/hooks/use-other-user";
import { format } from "date-fns";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { useCallback, useMemo } from "react";
interface ConversationBoxProps {
    conversation: Conversation;
    selected: boolean;
}

const ConversationBox = ({conversation, selected}: ConversationBoxProps) => {
    const otherUser = useOtherUser(conversation);
    const router = useRouter();
    const { session } = useSession();
   


  const handleClick = useCallback(() => {
    router.push(`/conversations/${conversation.id}`);
  }, [conversation, router]);



  const userEmail = useMemo(() => session?.user?.emailAddresses[0]?.emailAddress,
  [session?.user?.emailAddresses]);


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