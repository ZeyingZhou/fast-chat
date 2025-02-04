import NextAuth from "next-auth"
import authConfig from "./auth.config"

const { auth } = NextAuth(authConfig)

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const { nextUrl } = req

  const isApiRoute = nextUrl.pathname.startsWith('/api/')
  const isAuthRoute = nextUrl.pathname.startsWith('/signin') || 
                     nextUrl.pathname.startsWith('/signup') ||
                     nextUrl.pathname.startsWith('/verify-email')

  if (isAuthRoute) {
    if (isLoggedIn) {
      return Response.redirect(new URL('/conversations', nextUrl))
    }
    return null as unknown as Response
  }

  if (!isLoggedIn && !isApiRoute) {
    return Response.redirect(new URL('/signin', nextUrl))
  }

  return null as unknown as Response
})

// Optionally, don't invoke Middleware on some paths
export const config = {
  matcher: [
    "/((?!.+\\.[\\w]+$|_next).*)", "/", "/(api|trpc)(.*)"],
}