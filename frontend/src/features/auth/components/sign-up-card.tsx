'use client'
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { TriangleAlert } from 'lucide-react';



export const SignUpCard = () => {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmpassword, setConfirmPassword] = useState("");
  const [error, setError] = useState('');
  const [pending, setPending] = useState(false);



  return (
    <Card className="w-full h-full p-8 border-none">
    <CardHeader className="px-0 pt-0 items-center">
        <Image src="/fast-chat-logo.svg" width={100} height={100} alt="Logo"/>
        <CardTitle>
            Sign up to continue
        </CardTitle>
        <CardDescription>
        Use your email or another service to continue
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
                disabled={false}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Full name"
                required
            />
            <Input
                disabled={false}
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
               <Input
                disabled={pending}
                value={confirmpassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm password"
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
        {/* <div className="flex flex-col gap-y-2.5">
            <Button
                disabled={false}
                onClick={() => onProviderSignUp("google")}
                variant="outline"
                size="lg"
                className="w-full relative"
            >
                <FcGoogle className="size-5 absolute top-2.5 left-2.5"/>
                Continue with Google
            </Button>
            <Button
                disabled={false}
                onClick={() => onProviderSignUp("github")}
                variant="outline"
                size="lg"
                className="w-full relative"
            >
                <FaGithub className="size-5 absolute top-3 left-2.5"/>
                Continue with Github
            </Button>
        </div> */}
        <p className="text-xs text-muted-foreground">
            Already have an account? <span onClick={() => router.push('/signin')} className="text-sky-700 hover:underline cursor-pointer">Sign in</span>
        </p>
    </CardContent>
</Card>
  );
}