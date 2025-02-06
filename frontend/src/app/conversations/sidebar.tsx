import { UserButton } from "@clerk/nextjs";
import MobileFooter from "./mobile-footer";
import DesktopSidebar from "./desktop-siderbar";
import { currentUser } from '@clerk/nextjs/server'

const Sidebar = async ({children}: {children: React.ReactNode}) => {
    const user = await currentUser();
    
    const userData = user ? {
        id: user.id,
        name: `${user.firstName} ${user.lastName}`.trim() || null,
        email: user.emailAddresses[0]?.emailAddress,
        imageUrl: user.imageUrl,
    } : null;

    return ( 
        <div className="flex flex-col h-full">
            <DesktopSidebar currentUser={userData}/>
            <MobileFooter/>
            {children}
        </div>
    );
}

export default Sidebar;