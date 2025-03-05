"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { User } from "@/types";

export default function AvatarGroup({users}: {users: User[]}) {

  return (
    <div className="flex items-center -space-x-2 *:ring-3 *:ring-background">
      {users.slice(0, 4).map((user, index) => (
        <Avatar
          key={index}
        >
          <AvatarImage src={user.image} alt={user.name} />
          <AvatarFallback>
            {user.name
              .split(" ")
              .map((n) => n[0])
              .join("")}
          </AvatarFallback>
        </Avatar>
      ))}
      {users.length > 4 && (
        <Avatar className="z-10 text-sm font-medium text-muted-foreground">
          <AvatarFallback>
            +{users.length - 4}
          </AvatarFallback>
        </Avatar>
      )}
    </div>
  );
}
