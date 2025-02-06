import { UserButton } from "@clerk/nextjs";

const ConversationsPage = () => {
    return ( 
        <div>
            <div className="flex justify-between items-center">
                <h1>Conversations</h1>
                <UserButton />
            </div>
        </div>
     );
}
export default ConversationsPage;