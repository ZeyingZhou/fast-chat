import { useSession } from "@clerk/nextjs";
import { useMemo } from "react";
import { Conversation } from "@/types";

const useOtherUser = (conversation: Conversation) => {
  const { session } = useSession();

  const otherUser = useMemo(() => {
    const currentUserEmail = session?.user.emailAddresses[0].emailAddress;

    const otherUser = conversation.users.filter((user) => user.email !== currentUserEmail);

    return otherUser[0];
  }, [session?.user.emailAddresses[0].emailAddress, conversation.users]);

  return otherUser;
};

export default useOtherUser;
