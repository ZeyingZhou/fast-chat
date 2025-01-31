// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const isPublicPage = (pathname: string) => {
  return pathname === '/auth';
};

export function middleware(request: NextRequest) {
  const storedAuth = request.cookies.get('auth-storage')?.value;
  const token = storedAuth ? JSON.parse(storedAuth)?.state?.token : null;

  if (!isPublicPage(request.nextUrl.pathname) && !token) {
    return NextResponse.redirect(new URL('/auth', request.url));
  }

  if (isPublicPage(request.nextUrl.pathname) && token) {
    return NextResponse.redirect(new URL('/', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};