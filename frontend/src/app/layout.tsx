import "./globals.css";
import { Inter } from 'next/font/google'
import {
  ClerkProvider,
} from '@clerk/nextjs'
import { SocketProvider } from '@/providers/socket-provider';



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
          <SocketProvider>
            {children}
          </SocketProvider>
        </body>
      </html>
      </ClerkProvider>
    );
  }
