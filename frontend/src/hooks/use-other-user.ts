import { useSession } from "@clerk/nextjs";
import { useMemo } from "react";
import { FullConversationType } from "../../types";
import { User } from "../../types";

const useOtherUser = (conversation: FullConversationType | { users: User[] }) => {
  const { session } = useSession();

  const otherUser = useMemo(() => {
    const currentUserEmail = session?.user.emailAddresses[0].emailAddress;
    const otherUser = conversation.users.filter((user) => user.email !== currentUserEmail);
    
    return otherUser[0];
  }, [session?.user.emailAddresses[0].emailAddress, conversation.users]);
  return otherUser;
};

export default useOtherUser;
