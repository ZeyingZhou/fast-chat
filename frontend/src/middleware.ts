import { RedirectToSignIn } from "@clerk/nextjs";
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const publicRoutes = createRouteMatcher(['/sign-in(.*)', '/sign-up(.*)'])
const protectedRoutes = createRouteMatcher(['/conversations(.*)'])

export default clerkMiddleware(async (auth, request) => {
  const { userId } = await auth()
  const {pathname} = request.nextUrl

  if (!userId) {
    // Allow access to public routes
    if (publicRoutes(request)) {
      return NextResponse.next();
    }
    
    // Redirect to sign-in for protected routes
    RedirectToSignIn
 
  }

  if (userId) {
    // Redirect from auth pages to conversations
    if (publicRoutes(request)) {
      return NextResponse.redirect(new URL('/conversations', request.url));
    }

    // Redirect from root to conversations
    if (pathname === '/') {
      return NextResponse.redirect(new URL('/conversations', request.url));
    }

    // Protect routes that require authentication
    if (protectedRoutes(request)) {
      await auth.protect();
    }
  }
  return NextResponse.next()
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(.*)',
  ],
};