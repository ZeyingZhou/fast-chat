"use client";
import { useState } from "react";
import GroupChatModal from "./group-chat-modal";
import { Conversation, User } from "../../../../types";
import { cn } from "../../../../lib/utils";
import { useRouter } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import useConversation from "@/hooks/use-conversation";
import { MdOutlineGroupAdd } from "react-icons/md";
import { useAuth } from "@clerk/nextjs";
import { useUser } from "@clerk/nextjs";
import ConversationBox from "./conversation-box";
interface ConversationListProps {
    conversations: Conversation[];
    users: User[];
    title?: string;
}
const ConversationList = ({conversations, users, title}: ConversationListProps) => {
    const [items, setItems] = useState<Conversation[]>(conversations);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const router = useRouter();
    const session = useAuth();
    const user = useUser();

    const {conversationId, isOpen} = useConversation();

    return ( 
        <>
        {/* <GroupChatModal 
          users={users} 
          isOpen={isModalOpen} 
          onClose={() => setIsModalOpen(false)}
        /> */}
        <aside className={cn(`
          fixed 
          inset-y-0 
          pb-20
          h-full
          lg:pb-0
          lg:left-20 
          lg:w-96
          lg:block
          overflow-y-auto 
          border-r 
          border-gray-200 
        `, isOpen ? 'hidden' : 'block w-full left-0')}>
          <div className="px-5">
            <div className="flex justify-between mb-4 pt-4">
              <div className="text-2xl font-bold text-neutral-800">
                Messages
              </div>
              <div 
                onClick={() => setIsModalOpen(true)} 
                className="
                  rounded-full 
                  p-2 
                  bg-gray-100 
                  text-gray-600 
                  cursor-pointer 
                  hover:opacity-75 
                  transition
                "
              >
                <MdOutlineGroupAdd size={20} />
              </div>
            </div>
            {items.map((item) => (
              <ConversationBox
                key={item.id}
                conversation={item}
                selected={conversationId === item.id}
              />
            ))}
          </div>
        </aside>
      </>
     );
}

export default ConversationList;