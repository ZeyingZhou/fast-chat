"use client"
import {Loader, LogOut} from "lucide-react";

import {
    Avatar,
    AvatarFallback,
    AvatarImage
} from "@/components/ui/avatar";

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import { useAuth } from "@/hooks/use-auth";


export const UserButton = () => {
    const { user, signOut, isLoading } = useAuth()
    const handleSignOut = async () => {
        // Clear tokens from local storage or cookies (if applicable)
        localStorage.removeItem("convex_auth_token");
        sessionStorage.removeItem("convex_auth_token");
        // Call Convex's sign-out method
        await signOut();
      };


    if(isLoading) {
        return <Loader className="size-4 animate-spin text-muted-foreground"></Loader>
    }

    if(!user) {
        return null;
    }

    const { image, name, email } = user;

    const avatarFallback = name!.charAt(0).toUpperCase();


    return (
        <DropdownMenu modal={false}>
            <DropdownMenuTrigger className="outline-none relative">
                <Avatar className="rounded-md size-10 hover:opacity-75 transition">
                    <AvatarImage className="rounded-md" alt={name || undefined} src={image || undefined} />
                    <AvatarFallback className="rounded-md bg-sky-500 text-white">
                        {avatarFallback}
                    </AvatarFallback>
                </Avatar>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="center" side="right" className="w-60">
                <DropdownMenuItem onClick={() => handleSignOut()} className="h-10">
                    <LogOut className="size-4 mr-2"/>
                    Log out
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}