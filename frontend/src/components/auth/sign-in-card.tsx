'use client'

import * as z from "zod"
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Image from "next/image"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { LoginSchema } from "@/schemas/auth"
import { login } from "@/actions/auth"
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { TriangleAlert } from "lucide-react"
import { Separator } from "@/components/ui/separator"

export const SignInCard = () => {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [isPending, setIsPending] = useState(false)

  const { register, formState: { errors }, handleSubmit } = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  const onSubmit = async (values: z.infer<typeof LoginSchema>) => {
    setError(null)
    setIsPending(true)

    try {
      const result = await login(values)

      if (result?.error) {
        setError(result.error)
        return
      }

      if (result?.success) {
        router.push('/conversations')
        router.refresh()
      }
    } finally {
      setIsPending(false)
    }
  }

  return (
    <Card className="w-full h-full p-8 border-none">
      <CardHeader className="px-0 pt-0 items-center">
        <Image src="/fast-chat-logo.svg" width={60} height={60} alt="Logo"/>
        <CardTitle>
          Fast Chat
        </CardTitle>
        <CardDescription>
          Let's chat
        </CardDescription>
      </CardHeader>
      
      {error && (
        <div className="bg-destructive/15 p-3 rounded-md flex items-center gap-x-2 text-sm text-destructive mb-6">
          <TriangleAlert className="size-4"/>
          <p>{error}</p>
        </div>
      )}

      <CardContent className="space-y-5 px-0 pb-0">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-2.5">
          <div className="flex flex-col gap-y-2.5 mb-5">
            <div>
              <Input
                disabled={isPending}
                placeholder="Email"
                type="email"
                {...register("email")}
              />
              {errors.email && (
                <p className="text-xs text-red-600 mt-1">
                  {errors.email.message}
                </p>
              )}
            </div>

            <div>
              <Input
                disabled={isPending}
                placeholder="Password"
                type="password"
                {...register("password")}
              />
              {errors.password && (
                <p className="text-xs text-red-600 mt-1">
                  {errors.password.message}
                </p>
              )}
            </div>
          </div>

          <div className="flex justify-center">
            <Button 
              variant="fastchat" 
              type="submit" 
              className="rounded-full p-5" 
              size="lg" 
              disabled={isPending}
            >
              {isPending ? "Signing in..." : "Continue"}
            </Button>
          </div>
        </form>

        <Separator/>

        <p className="text-xs text-muted-foreground">
          Don't have an account? {" "}
          <span 
            onClick={() => router.push('/signup')} 
            className="text-sky-700 hover:underline cursor-pointer"
          >
            Sign up
          </span>
        </p>
      </CardContent>
    </Card>
  )
}