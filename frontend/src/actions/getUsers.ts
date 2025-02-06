import { clerkClient } from "@clerk/express";

const getUsers = async () => {
    const response = await clerkClient.;
    return response.data;
}

export default getUsers;