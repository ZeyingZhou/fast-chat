"use client"
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useEffect } from "react";



export default function Home() {
  const router = useRouter();
  // useEffect(() => {
  //   const fetchUser = async () => {
  //     const user = await fetch('http://localhost:8000/users/me');
  //     console.log(user);
  //   };
  //   fetchUser();
  // }, []);

  return (
      <main className="flex h-full flex-col items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-sky-400 to-blue-800">
        <h1>Hello</h1>
      </main>
  );
}
