import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";
import { IconType } from "react-icons/lib";
import Link from "next/link";

interface DesktopItemProps {
    label: string;
    icon: LucideIcon | IconType;
    href: string;
    onClick?: () => void;
    isActive?: boolean;
}

export const DesktopItem = ({
    label,
    icon: Icon,
    href,
    onClick,
    isActive
}: DesktopItemProps) => {
    const handleClick = () => {
        if (onClick) {
          return onClick();
        }
      };
    return (
        <li onClick={handleClick} key={label}>
            <Link
                href={href}
                className={cn(
                    "group flex gap-x-3 rounded-md p-3 text-sm leading-6 font-semibold text-gray-500 hover:text-black hover:bg-gray-100",
                    isActive && "bg-gray-100 text-black"
                )}
            >
                <Icon className="h-6 w-6 shrink-0" aria-hidden="true"/>
            </Link>
            <span className="text-[11px] text-white group-hover:text-accent">
                {label}
            </span>
        </li>
    )
};