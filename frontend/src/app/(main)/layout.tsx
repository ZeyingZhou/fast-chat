import Sidebar from "./conversations/components/sidebar";

const MainLayout = ({children}: {children: React.ReactNode}) => {
    return ( 
            <Sidebar>
                    {children}
            </Sidebar>
    );
}

export default MainLayout;