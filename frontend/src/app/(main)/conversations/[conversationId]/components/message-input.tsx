'use client';

import { Input } from "@/components/ui/input";
import { Smile } from "lucide-react";
import { 
  FieldErrors, 
  FieldValues, 
  UseFormRegister
} from "react-hook-form";
import { EmojiPopover } from "./emoji-popover";
import { Button } from "@/components/ui/button";

interface MessageInputProps {
  placeholder?: string;
  id: string;
  type?: string;
  required?: boolean;
  register: UseFormRegister<FieldValues>,
  errors: FieldErrors,
  onEmojiSelect: (emoji: string) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({ 
  placeholder, 
  id, 
  type, 
  required, 
  register, 
  onEmojiSelect
}) => {
  return (
    <div className="relative w-full">
      <Input
        id={id}
        type={type}
        autoComplete={id}
        {...register(id, { required })}
        placeholder={placeholder}
        className="
          text-black
          font-light
          py-2
          px-4
          bg-neutral-100 
          w-full 
          rounded-full
          focus:outline-none
        "
      />
      <div className="absolute right-2 top-1/2 -translate-y-1/2">
        <EmojiPopover onEmojiSelect={onEmojiSelect}>
            <Button 
              disabled={false}
              size="sm"
              variant="ghost"
              className="rounded-full hover:bg-neutral-200"
            >
              <Smile   className="
                    text-sky-500
                    cursor-pointer
                    hover:text-sky-600
                    transition
                    "/>
          </Button>
        </EmojiPopover>
    </div>
    </div>
   );
}
 
export default MessageInput;