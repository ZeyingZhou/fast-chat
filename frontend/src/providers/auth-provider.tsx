'use client';

import { useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { token, fetchUser } = useAuthStore();

  useEffect(() => {
    // Verify token and fetch user data on initial load
    if (token) {
      fetchUser().catch(() => {
        useAuthStore.getState().signOut();
        if (!isPublicRoute(pathname)) {
          router.push('/sign-in');
        }
      });
    }
  }, [token]);

  const isPublicRoute = (path: string) => {
    return path === '/sign-in' || path === '/sign-up';
  };

  return <>{children}</>;
}