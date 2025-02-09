import Sidebar from "./conversations/components/sidebar";

const MainLayout = ({children}: {children: React.ReactNode}) => {
    return ( 
        <Sidebar>
            <div className="h-full">
                {children}
            </div>
        </Sidebar>
    );
}

export default MainLayout;