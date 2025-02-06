'use client'

import { useSession, signOut } from 'next-auth/react'
import { useRouter } from 'next/navigation'

export function useAuth() {
  const router = useRouter()
  const { data: session, status } = useSession()

  const handleSignOut = async () => {
    await signOut({ redirect: false })
    router.push('/signin')
  }

  return {
    user: session?.user,
    isLoading: status === 'loading',
    isAuthenticated: status === 'authenticated',
    signOut: handleSignOut,
  }
}