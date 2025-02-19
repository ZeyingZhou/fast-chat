import { User } from "../../../../../types";

interface GroupChatModalProps {
    users: User[];
    isOpen: boolean;
    onClose: () => void;
}

const GroupChatModal = ({isOpen, onClose}: GroupChatModalProps) => {
    return ( 
        <div>
            GroupChatModal
        </div>
     );
}
 
export default GroupChatModal;