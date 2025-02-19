"use client";
import useOtherUser from "@/hooks/use-other-user";
import { Conversation, User } from "../../../../../../types";
import { useState } from "react";
import useActiveList from "@/hooks/use-active-list";
import { useMemo } from "react";
import { ChevronLeft, ChevronLeftIcon, EllipsisIcon, Link } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface HeaderProps {
    conversation: Conversation & {
        users: User[]; 
    };
}

const Header: React.FC<HeaderProps> = ({ conversation }) => {
    const otherUser = useOtherUser(conversation);
    const [drawerOpen, setDrawerOpen] = useState(false);

    const { members } = useActiveList();
    const isActive = members.indexOf(otherUser?.email!) !== -1;
    const statusText = useMemo(() => {
      if (conversation.isGroup) {
        return `${conversation.users.length} members`;
      }
  
      return isActive ? 'Active' : 'Offline'
    }, [conversation, isActive]);
    
    return ( 
        <>
            <div className="bg-white w-full flex border-b-[1px] sm:px-4 py-3 px-4 lg:px-6 justify-between items-center shadow-sm">
                <div className="flex gap-3 items-center">
                    <Link href="/conversations" className="lg:hidden block text-sky-500 hover:text-sky-600 transition cursor-pointer">
                        <ChevronLeftIcon className="size-6" />
                    </Link>
                    <Avatar className="size-8 mr-1">
                        <AvatarImage className="rounded-md" src={otherUser.image}/>
                        <AvatarFallback>
                            {otherUser.name?.charAt(0)}
                        </AvatarFallback>
                    </Avatar>
                    <div className="flex flex-col">
                        <div>{conversation.name || otherUser.name}</div>
                            <div className="text-sm font-light text-neutral-500">
                                {statusText}
                            </div>
                    </div>
                </div>
                <EllipsisIcon
                    size={32}
                    onClick={() => setDrawerOpen(true)}
                    className="
                    text-sky-500
                    cursor-pointer
                    hover:text-sky-600
                    transition
                    "
                />
            </div>
        </>
    );
}   

export default Header;