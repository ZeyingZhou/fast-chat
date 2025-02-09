import UserList from "./components/user-list";
import getUsers from "@/actions/get-users";

const UsersLayout = async ({children}: {children: React.ReactNode}) => {
    const users = await getUsers();
    return ( 
        <>
            <UserList items={users}/>
            {children}
        </>
    );
}

export default UsersLayout;