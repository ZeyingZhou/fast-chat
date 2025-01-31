"use client"
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useEffect } from "react";



export default function Home() {
  const router = useRouter();
  useEffect(() => {
    const fetchUser = async () => {
      const user = await fetch('http://localhost:8000/users/me');
      console.log(user);
    };
    fetchUser();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <Button variant="outline">Click me</Button>
    </div>
  );
}
