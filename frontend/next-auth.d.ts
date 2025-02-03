import { DefaultSession, DefaultUser } from "next-auth"


interface User {
  id: string
  email: string
  username: string
  image?: string
}

interface SignInResponse {
  user: User
  access_token: string
}
declare module "next-auth" {
  interface Session {
    accessToken?: string
    user: {
      id: string
      email: string
      name: string
      image?: string
    } & DefaultSession["user"]
  }
  export interface User {
    accessToken: string
    id: string
    email: string
    name: string
    image: string
  }
}

declare module "next-auth/jwt" {
  export interface JWT {
    accessToken: string
    id: string
    email: string
    name: string
    image: string
  }
}
