


interface ConversationIdPageProps {     
    params: {
        conversationId: string
    }
}

const ConversationIdPage: React.FC<ConversationIdPageProps> = ({ params }) => {
    return ( 
        <div>
            <h1>Conversation {params.conversationId}</h1>
        </div>
     );
}
 
export default ConversationIdPage;