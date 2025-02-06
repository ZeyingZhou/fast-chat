import { useMemo } from "react";
import { usePathname } from "next/navigation";
import { MessageCircleMore, Users, LogOut } from "lucide-react";
import { useClerk } from "@clerk/nextjs";
import useConversation from "./use-conversation";


const useRoutes = () => {
  const pathname = usePathname();
  const { signOut } = useClerk();
  const { conversationId } = useConversation();

  const routes = useMemo(() => [
    { 
      label: 'Chat', 
      href: '/conversations', 
      icon: MessageCircleMore,
      active: pathname === '/conversations' || !!conversationId
    },
    { 
      label: 'Users', 
      href: '/users', 
      icon: Users, 
      active: pathname === '/users'
    },
    {
      label: 'Logout', 
      onClick: () => signOut(),
      icon: LogOut, 
      href: '#',
    }
  ], [pathname, conversationId]);

  return routes;
};

export default useRoutes;
