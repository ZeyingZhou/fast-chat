"use client";

import { User } from "@/types";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { useEffect, useState } from "react";

export default function AvatarUser({user}: {user: User}) {
    // Start with empty fallback on server
    const [fallback, setFallback] = useState<string>("");
    
    // Only set the fallback on the client side
    useEffect(() => {
        if (user?.name) {
            setFallback(user.name.charAt(0).toUpperCase());
        } else {
            setFallback("?");
        }
    }, [user?.name]);
    
    return (
        <Avatar className="size-8 mr-1">
            <AvatarImage className="rounded-md" src={user.image} />
            <AvatarFallback>
                {fallback}
            </AvatarFallback>
        </Avatar>
    );
}   