import type { NextAuthConfig } from "next-auth"

if (!process.env.NEXTAUTH_SECRET) {
  throw new Error('Please set NEXTAUTH_SECRET environment variable')
}

if (!process.env.API_URL) {
  throw new Error('Please set API_URL environment variable')
}

export const authOptions: NextAuthConfig = {
  debug: process.env.NODE_ENV === 'development',
  pages: {
    signIn: '/signin',
  },
  providers: [],
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user
      const isOnAuth = nextUrl.pathname.startsWith('/signin')
      
      if (isOnAuth) {
        if (isLoggedIn) {
          return Response.redirect(new URL('/chat', nextUrl))
        }
        return true
      }

      if (!isLoggedIn) {
        return false
      }

      return true
    },
  },
} 