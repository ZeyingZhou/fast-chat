import { UserButton } from "@clerk/nextjs";
import { useParams } from "next/navigation";

interface ConversationIdPageProps {     
    params: {
        conversationId: string
    }
}

const ConversationIdPage: React.FC<ConversationIdPageProps> = ({ params }) => {
    const conversationId = useParams();
    return ( 
        <div>
            <h1>Conversation {params.conversationId}</h1>
            <UserButton />
        </div>
     );
}
 
export default ConversationIdPage;