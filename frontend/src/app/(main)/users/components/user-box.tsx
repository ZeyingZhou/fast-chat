import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { User } from "../../../../../types";
import { Loader } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState, useCallback } from "react";

interface UserBoxProps {
    data: User
}

const UserBox = ({data}: UserBoxProps) => {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    
    const handleClick = useCallback(async () => {
            setIsLoading(true);
            fetch('/api/conversations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: data.id
                })
            })
            .then((data) => {
                router.push(`/conversations`);
            })
            .finally(() => setIsLoading(false));
    }, [data, router]);
    
    return ( 
        <>
            {isLoading && (
                <div className="flex items-center justify-center h-full">
                    <Loader className="animate-spin size-10 text-gray-500" />
                </div>
            )}
              <div
        onClick={handleClick}
        className="
          w-full 
          relative 
          flex 
          items-center 
          space-x-3 
          bg-white 
          p-3 
          hover:bg-neutral-100
          rounded-lg
          transition
          cursor-pointer
        "
      >
        <Avatar className="size-5 mr-1">
            <AvatarImage className="rounded-md" src={data.image}/>
            <AvatarFallback>
                {data.name?.charAt(0)}
            </AvatarFallback>
        </Avatar>
        <div className="min-w-0 flex-1">
          <div className="focus:outline-none">
            <span className="absolute inset-0" aria-hidden="true" />
            <div className="flex justify-between items-center mb-1">
              <p className="text-sm font-medium text-gray-900">
                {data.name}
              </p>
            </div>
          </div>
        </div>
      </div>
        </>
    );
}

export default UserBox;