'use client'
import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Image from "next/image";
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { TriangleAlert } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { signIn } from 'next-auth/react';

export const SignInCard = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null)
  const [pending, setPending] = useState(false);
  
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
            {!!error && (
                <div className="bg-destructive/15 p-3 rounded-md flex items-center gap-x-2 text-sm text-destructive mb-6">
                    <TriangleAlert className="size-4"/>
                    <p>{error}</p>
                </div>
            )}
            <CardContent className="space-y-5 px-0 pb-0">
                <form onSubmit={() => {}} className="space-y-2.5">
                    <div className="flex flex-col gap-y-2.5 mb-5">
                        <Input
                            disabled={pending}
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Email"
                            type="email"
                            required
                        />
                        <Input
                            disabled={pending}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Password"
                            type="password"
                            required
                        />
                    </div>
                    <div className="flex justify-center">
                        <Button variant="fastchat" type="submit" className="rounded-full p-5" size="lg" disabled={false}>
                            Continue
                        </Button>
                    </div>
                </form>
                <Separator/>


                <p className="text-xs text-muted-foreground">
                    Don't have an account? <span onClick={() => router.push('/signup')} className="text-sky-700 hover:underline cursor-pointer">Sign up</span>
                </p>
            </CardContent>
        </Card>
  );
}