"use server"

import { signIn } from "@/auth"
import { LoginSchema, RegisterSchema } from "@/schemas/auth"
import { db } from "@/lib/prismadb"
import { AuthError } from "next-auth"
import bcrypt from "bcryptjs"
import * as z from "zod"
import { generateVerificationToken } from "@/lib/tokens"
import { sendVerificationEmail } from "@/lib/mail"
import { getUserByEmail } from "./user"


export async function login(values: z.infer<typeof LoginSchema>) {
  const validatedFields = LoginSchema.safeParse(values)

  if (!validatedFields.success) {
    return { error: "Invalid fields!" }
  }

  const { email, password } = validatedFields.data

  // Check if user exists and email is verified
  const existingUser = await db.user.findUnique({
    where: { email }
  });

  if (!existingUser?.emailVerified) {
    // Generate new verification token
    const verificationToken = await generateVerificationToken(email);
    
    // Send verification email again
    await sendVerificationEmail(
      verificationToken.email,
      verificationToken.token,
    );

    return { error: "Please verify your email first! We have sent you a new verification email." }
  }

  try {
    await signIn("credentials", {
      email,
      password,
      redirect: false,
    })

    return { success: true }
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case "CredentialsSignin":
          return { error: "Invalid email or password" }
        default:
          return { error: "Something went wrong" }
      }
    }

    throw error
  }
}

export async function register(values: z.infer<typeof RegisterSchema>) {
  const validatedFields = RegisterSchema.safeParse(values)

  if (!validatedFields.success) {
    return { error: "Invalid fields!" }
  }

  const { email, password, name } = validatedFields.data

  const existingUser = await db.user.findUnique({
    where: { email },
  })

  if (existingUser) {
    return { error: "Email already in use" }
  }

  const hashedPassword = await bcrypt.hash(password, 10)

  const user = await db.user.create({
    data: {
      email,
      name,
      password: hashedPassword,
      emailVerified: null,
    },
  })

  // Generate verification token
  const verificationToken = await generateVerificationToken(email);
  
  // Send verification email
  await sendVerificationEmail(
    verificationToken.email,
    verificationToken.token,
  );

  return { success: true }
}

export async function verifyEmail(token: string) {
  try {
    const existingToken = await db.verificationToken.findUnique({
      where: { token }
    });

    if (!existingToken) {
      return { error: "Token does not exist!" };
    }

    const hasExpired = new Date(existingToken.expires) < new Date();

    if (hasExpired) {
      return { error: "Token has expired!" };
    }

    const user = await getUserByEmail(existingToken.email);

    if (!user) {
      return { error: "Email does not exist!" };
    }

    await db.user.update({
      where: { id: user.id },
      data: { 
        emailVerified: new Date(),
      }
    });

    await db.verificationToken.delete({
      where: { id: existingToken.id }
    });

    return { success: "Email verified" };
  } catch {
    return { error: "Something went wrong!" }
  }
}