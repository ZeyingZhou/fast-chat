import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarTrigger,
  } from "@/components/ui/sidebar"
import { UserButton } from "@clerk/nextjs";
import { VisuallyHidden } from "@radix-ui/react-visually-hidden";
import { MessageCircle } from "lucide-react";

export const CustomSidebar = () => {
    return (
      <Sidebar collapsible="icon" side="left" className="dark">
      <SidebarContent>
        <VisuallyHidden>
          <SidebarHeader>
            Fast Chat
          </SidebarHeader>
        </VisuallyHidden>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a>
                  <MessageCircle/>
                  <span>Conversations</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <UserButton />
        <SidebarTrigger />
      </SidebarFooter>
    </Sidebar>
    )
}
  