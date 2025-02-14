"use client";

import useRoutes from "@/hooks/use-routes";
import { User } from "@clerk/nextjs/server";
import { useState } from "react";
import { DesktopItem } from "./desktop-item";
import { Avatar } from "@/components/ui/avatar";

import dynamic from "next/dynamic";

const UserButton = dynamic(() => import("@clerk/nextjs").then((mod) => mod.UserButton), {
  ssr: false,
});


interface DesktopSidebarProps {
    currentUser: {
        id: string;
        name?: string | null;
        email?: string;
        imageUrl?: string;
    } | null;
}

const DesktopSidebar = ({currentUser}: DesktopSidebarProps) => {
    const routes = useRoutes();
    const [isOpen, setIsOpen] = useState(false);
    return ( 
        <div className="
        hidden 
        lg:fixed 
        lg:inset-y-0 
        lg:left-0 
        lg:z-40 
        lg:w-20 
        xl:px-6
        lg:overflow-y-auto 
        lg:bg-white 
        lg:border-r-[1px]
        lg:pb-4
        lg:flex
        lg:flex-col
        justify-between
      ">
        <nav className="mt-4 flex flex-col justify-between">
          <ul role="list" className="flex flex-col items-center space-y-1">
            {routes.map((item) => (
              <DesktopItem
                key={item.label}
                href={item.href}
                label={item.label}
                icon={item.icon}
                isActive={item.active}
                onClick={item.onClick}
              />
            ))}
          </ul>
        </nav>
        <nav className="mt-4 flex flex-col justify-between items-center">
          <div 
            className="cursor-pointer hover:opacity-75 transition"
          >
            <UserButton/>
          </div>
        </nav>
        </div>
     );
}
 
export default DesktopSidebar;