import "./globals.css";
import { Inter } from 'next/font/google'
import {
  ClerkProvider,
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs'
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";


const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider afterSignOutUrl="/sign-in">
    <html lang="en">
      <body className={inter.className}>   
          {children}   
      </body>
    </html>
    </ClerkProvider>
  );
}
