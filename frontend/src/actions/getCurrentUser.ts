import { currentUser } from "@clerk/nextjs/server";

const getCurrentUser = async () => {
    const user = await currentUser();
    if (!user) {
        return null;
    }
    return user;
}

export default getCurrentUser;