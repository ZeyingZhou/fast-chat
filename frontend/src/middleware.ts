import NextAuth from "next-auth"
import { authOptions } from "./lib/auth.config"

export const middleware = NextAuth(authOptions).auth

export const config = {
  matcher: [
    '/chat/:path*',
    '/api/chat/:path*',
    '/((?!api|_next/static|_next/image|images|favicon.ico|.*\\.svg|signin|signup).*)',
  ]
}