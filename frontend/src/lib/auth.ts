import NextAuth, { Session } from "next-auth"
import { User } from "next-auth"
import { JWT } from "next-auth/jwt"
import { authOptions } from "./auth.config"
import Credentials from "next-auth/providers/credentials"

interface SignInResponse {
  access_token: string
  token_type: string
  user: {
    id: string
    email: string
    username: string
    image?: string
  }
}

export const { handlers: { GET, POST }, auth, signIn, signOut } = NextAuth({
  ...authOptions,
  session: { strategy: "jwt" },
  providers: [
    Credentials({
      id: 'credentials',
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          throw new Error('Please enter your email and password')
        }
        if (typeof credentials.email !== 'string' || typeof credentials.password !== 'string') {
          throw new Error('Email and password must be strings')
        }  
        try {
          const formData = new URLSearchParams()
          formData.append('email', credentials.email)
          formData.append('password', credentials.password)
          
          const response = await fetch(`${process.env.API_URL}/signin`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData.toString(),
          })

          if (!response.ok) {
            throw new Error('Invalid credentials')
          }
          
          const data = await response.json()
          
          return {
            id: data.user.id,
            email: data.user.email,
            name: data.user.username,
            image: data.user.image,
            accessToken: data.access_token,
          }
        } catch (error) {
          console.error('Auth error:', error)
          throw error
        }
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }: { token: JWT, user?: User }) {
      if (user) {
        return {
          ...token,
          accessToken: user.accessToken,
          id: user.id,
          email: user.email,
          name: user.name,
          image: user.image || '',
        } as JWT
      }
      return token
    },
    async session({ session, token }: { session: Session, token: JWT }) {
      if (token) {
        // Ensure type safety by providing default values or type guards
        session.accessToken = token.accessToken ?? undefined
        session.user.id = token.id ?? '' // or provide a default value that makes sense for your app
      }
      return session
    }
  }
})